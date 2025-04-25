import click
import argparse
import os
import subprocess
import signal

import itertools
import threading
import time
import sys

from .general import sync_policies, sync_profiles_from_tar, check_cinc_installed, check_saf_installed
from .static import static_analysis
from .provision import install_cinc, install_train_plugin
from .generate import generate_input_file
from .review import validate_file, create_output_rollup
from anchorestig import __version__

@click.group()
def main():
    pass


@click.command()
@click.option('--username', '-u', help='Username for private registry')
@click.option('--password', '-p', help="Password for private registry")
@click.option('--url', '-r', help="URL for private registry")
@click.option('--aws-bucket', '-b', help="S3 upload. Specify bucket name")
@click.option('--account', '-a', help="Anchore STIG UI account. Required for S3 upload")
@click.option('--insecure', '-s', is_flag=True, default=False, help="Allow insecure registries or registries with custom certs")
@click.option('--profile', '-l', default="auto", help="Specify profile to run. Can be the name of an existing profile or the path to a custom profile")
@click.option('--input-file', '-i', help="Specify the path to a custom input file to run with a profile.")
@click.option('--sync', '-y', is_flag=True, default=False, help="Sync policies from Anchore")
@click.option('--sync-from-file', '-t', help="Sync policies from tar file provided by Anchore. Provide the path to the tar file.")
@click.argument('image')
def static(username, password, url, insecure, image, aws_bucket, account, profile, input_file, sync, sync_from_file):
    """Run static analysis"""
    if sync:
        sync_policies()
        print("Policies successfully downloaded.")
    if sync_from_file:
        sync_profiles_from_tar(sync_from_file)
        print("Policies successfully updated.")
    check_cinc_installed()
    check_saf_installed()
    if not input_file:
        input_file = "default"
    stop_spinner = threading.Event()
    def animate():
        spinner = ['|', '/', '-', '\\']
        i = 0
        try:
            while not stop_spinner.is_set():  # Check if the stop_event is set
                print(f'\r{spinner[i % len(spinner)]}', end='', flush=True)
                time.sleep(0.1)
                i += 1
        finally:
            print("\rProcess complete.")

    spinner_thread = threading.Thread(target=animate)
    spinner_thread.start()
    aws = aws_bucket
    try:
        static_analysis(username, password, url, insecure, image, aws, account, profile, input_file)
    except:
        sys.exit(1)
    finally:
        stop_spinner.set()
        spinner_thread.join()

@click.command()
def runtime():
    print("Please contact Anchore Sales for access to Anchore's Runtime STIG offering.")

@click.command()
def vm():
    print("Please contact Anchore Sales for access to Anchore's VM STIG offering.")

@click.command()
@click.option('--install', '-i', is_flag=True, default=False, help="Install the necessary version of CINC")
@click.option("--privileged", "-s", is_flag=True, default=False, help="Install CINC with sudo.")
@click.option("--plugin", "-p", is_flag=True, default=False, help="Install the CINC Train K8S Plugin")
def provision(install, privileged, plugin):
    """Install required tools. Please note this tool is experimental. Refer to documentation for instructions about installing required tooling."""
    if install:
        install_cinc(privileged)
    if plugin:
        install_train_plugin()

@click.command()
@click.argument('profile_name', required=False)
def generate(profile_name):
    """Generate an example inputs file. Note: the generated file will be the default file used if no input file is specified."""
    profile_list = """
    Profile name required. Please specify one of the following as an argument.
    Available profile names:
    apache-tomcat9
    crunchy-postgresql
    jboss
    jre7
    mongodb
    nginx
    postgres9
    ubi8
    ubi9
    ubuntu2004
    ubuntu2204
    ubuntu2404
    """
    available_profiles = ["apache-tomcat9", "crunchy-postgresql", "jboss", "jre7", "mongodb", "nginx", "postgres9", "ubi8", "ubi9", "ubuntu2004", "ubuntu2204", "ubuntu2404"]
    if not profile_name:
        print(profile_list)
    elif profile_name not in available_profiles:
        print(profile_list)
    else:
        generate_input_file(profile_name)

@click.command()
@click.argument('output_file_path', required=True)
def review(output_file_path):
    """Generates an in-terminal rollup of a STIG result file"""
    valid_file = validate_file(output_file_path)
    if not valid_file:
        print("Input file is not valid, please try again.")
        exit()
    else:
        create_output_rollup(output_file_path)

@click.command()
def version():
    """Print the current version of Anchore STIG"""
    print(__version__)

main.add_command(static)
main.add_command(runtime)
main.add_command(vm)
main.add_command(provision)
main.add_command(generate)
main.add_command(version)


if __name__ == '__main__':
    main()
