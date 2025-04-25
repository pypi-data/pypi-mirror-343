import argparse
import os
import subprocess
import signal
import boto3
import importlib.util
import datetime
import itertools
import threading
import time
import sys
import re
import tarfile
from botocore.exceptions import NoCredentialsError, ClientError

def usage():
    print("Usage: anchorestig static <IMAGE> [-u registry_username] [-p registry_password] [-r registry_url] [-s] [-b AWS S3 Bucket name] [-a Anchore STIG UI Account] [-l STIG Profile nae or path] [-i Input File for STIG]")
    exit(1)

def stop_container(container_id):
    command = ['docker', 'kill', container_id]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
    except Exception:
        print(f"Unable to stop sandbox container. Please manually stop the container")

def add_date_prefix(filename):
    date_prefix = str(datetime.datetime.now().timestamp()).replace(" ", "_").split(".")[0]
    split_filename = filename.rsplit(".", 1)
    return split_filename[0] + date_prefix + "." + split_filename[-1]

def upload_to_s3(bucket_name, file, account, image_digest, image_name):
    """
    Upload files from a specified directory to an AWS S3 bucket.

    :param bucket_name: Name of the S3 bucket.
    :param directory: Directory containing files to upload.
    """
    # Check if the directory exists
    if not os.path.exists(file):
        print(f"Error: output directory does not exist.")
        return

    # Initialize S3 client with custom credentials
    if "@" in image_name:
        image_name = image_name.split('@')[0] + "NOTAG"
    
    image_name = image_name.removeprefix('http://').removeprefix('https://')
    tag = image_name.split(':')[-1]
    registry = image_name.split('/', 1)[0]
    repository = image_name.split('/', 1)[-1].split(":")[0].replace("/", "-")

    if repository + ':' + tag == registry:
        registry = 'docker.io'

    s3 = boto3.client('s3')

    file_name = file.split("/")[-1]
    date_filename = add_date_prefix(file_name)

    try:
        # Walk through the directory and upload files
        file_path = f"anchore/{account}/{registry}/{repository}/{tag}/{image_digest}/{date_filename}"
        s3.upload_file(file, bucket_name, file_path)
    except NoCredentialsError:
        print("Error: AWS credentials not found.")
    except ClientError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(e)

def get_image_digest(image, username, password, url, insecure):
    try:
        if not username:
            pull_cmd = ["docker", "pull", image]
        else:
            subprocess.run(["docker", "--config", "./stig-docker-config", "login", url, "-u", username, "-p", password], check=True)
            pull_cmd = ["docker", "pull", image]

        # Try to pull the image
        pull_result = subprocess.run(pull_cmd, capture_output=True, text=True)
        if pull_result.returncode != 0:
            raise RuntimeError(f"Failed to pull image {image}: {pull_result.stderr.strip()}")

        # Try to inspect the image digest
        inspect_result = subprocess.run(["docker", "inspect", '--format={{index .RepoDigests 0}}', image], capture_output=True, text=True)
        if inspect_result.returncode != 0 or not inspect_result.stdout.strip():
            raise RuntimeError(f"Failed to inspect image {image}: {inspect_result.stderr.strip()}")

        # Extract and print the digest
        digest = inspect_result.stdout.strip().split('@')[-1].replace('"', '')

        return digest

    except Exception as e:
        print(f"Error: {e}")
        return None

def determine_base_image(container_id):
    try:
        response = subprocess.run(["docker", "exec", "-it", container_id, "cat", "/etc/os-release"], capture_output=True, text=True)
        base_distro = response.stdout
        pattern = r"PRETTY_NAME=(.*?)(?:\n|$)"
        match = re.search(pattern, base_distro, re.DOTALL)
        base_distro = match.group(1).strip().lower()
        if "red hat enterprise linux 8" in base_distro:
            return "ubi8"
        elif "red hat enterprise linux 9" in base_distro:
            return "ubi9"
        elif "ubuntu 20" in base_distro:
            return "ubuntu2004"
        elif "ubuntu 22" in base_distro:
            return "ubuntu2204"
        elif "ubuntu 24" in base_distro:
            return "ubuntu2404"
        else:
            return "indeterminate"
    except Exception:
        print("Failed to determine base distribution.")
        stop_container(container_id)
        exit()

def get_container_id(image):
    try:
        response = subprocess.run(["docker", "run", "-t", "-d", "--entrypoint=cat", image], capture_output=True, text=True)
        container_id = response.stdout.strip()
        return container_id
    except Exception:
        print("Failed to start target image. Please verify and retry.")
        exit()

def saf_convert_output(outfile):
    conversion_tools = [ 'hdf2xccdf', 'hdf2ckl', 'hdf2csv']

    split_outfile = outfile.split('/')[-1].split('.json')[0]

    for tool in conversion_tools:
        if tool == "hdf2xccdf":
            file_ending = ".xml"
        elif tool == "hdf2ckl":
            file_ending = ".ckl"
        else:
            file_ending = ".csv"
        conversion_cmd = f"saf convert {tool} -i {outfile} -o ./stig-results/{split_outfile.split('-output')[0]}/{split_outfile}{file_ending}" 
        try:
            # Run the chosen installation command
            response = subprocess.run(conversion_cmd, shell=True, check=True, capture_output=True)
            if response.stdout.decode('utf-8'):
                print("\r", response.stdout.strip().decode('utf-8'))
        except subprocess.CalledProcessError as e:
            print(f"Failed to convert {outfile} to {split_outfile}{file_ending}: {e}")

def run_stig(container_id, output_dir, image, policy_path, input_file):
    sanitized_image = image.replace("/", "-").replace(":", "-")
    try:
        if input_file == "default":
            command = [
                "cinc-auditor", "exec", policy_path, "-t", f"docker://{container_id}", 
                "--reporter=cli", f"json:./{output_dir}/{sanitized_image}-output.json"
            ]
        else:
            if not os.path.isfile(input_file):
                print(f"Input file: {input_file} does not exist. Please Retry.")
                stop_container(container_id)
                return
            else:
                command = [
                    "cinc-auditor", "exec", policy_path, "-t", f"docker://{container_id}", 
                    f"--input-file={input_file}", "--reporter=cli", f"json:./{output_dir}/{sanitized_image}-output.json"
                ]
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    except subprocess.CalledProcessError as e:
        if e.returncode != 100:
            print(f"\rFailed to run STIG:\nExit Code: {e.returncode}")
            print(f"Error output:\n{e}")
            print(e.output.decode('utf-8'))
            raise

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

    finally:
        stop_container(container_id)

def static_analysis(username, password, url, insecure, image, aws_s3_bucket_upload, account, profile, input_file):

    if not image:
        usage()

    dir_name = image.replace("/", "-").replace(":", "-")
    os.makedirs(f"stig-results/{dir_name}", exist_ok=True)

    container_id = get_container_id(image)

    if profile == "auto":
        profile = determine_base_image(container_id)
    if profile == "indeterminate":
        print("No automatic profile available, please specify a profile to continue.")
        exit(1)

    package_name = "anchorestigstatic"
    spec = importlib.util.find_spec(package_name)
    package_root_directory = os.path.dirname(spec.origin)

    if profile == "ubi8" or profile == "ubi9" or profile == "ubuntu2004" or profile == "ubuntu2204" or profile == "ubuntu2404" or profile == "nginx" or profile == "crunchy-postgresql" or profile == "jboss" or profile == "jre7" or profile == "mongodb" or profile == "postgres9":
        policy_path = f"{package_root_directory}/policies/{profile}/anchore-{profile}-disa-stig-1.0.0.tar.gz"
    else:
        policy_path = profile

    print("\r-------Run Parameters-------\n")
    print(f"Target Image: {image}")
    print(f"Profile: {profile}")
    print(f"Input File: {input_file}")
    print(f'Output File Path: ./stig-results/{dir_name}/{image.replace("/", "-").replace(":", "-")}-output.json')
    try:
        run_stig(container_id, f"stig-results/{dir_name}", image, policy_path, input_file)
        saf_convert_output(f'./stig-results/{dir_name}/{image.replace("/", "-").replace(":", "-")}-output.json')
    except:
        raise
               
    if aws_s3_bucket_upload:
        try:
            image_digest = get_image_digest(image, username, password, url, insecure)
            for file in os.listdir(f"{os.getcwd()}/stig-results/{dir_name}"):
                upload_to_s3(aws_s3_bucket_upload, f"stig-results/{dir_name}/{file}", account, image_digest, image)
        except Exception as e:
            print(e)
            raise
