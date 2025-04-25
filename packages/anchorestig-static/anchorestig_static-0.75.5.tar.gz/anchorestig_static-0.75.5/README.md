# Anchore STIG

Anchore STIG is a complete STIG solution that can be used to run STIG profile against static images.

## Description

Use Anchore STIG to perform STIG checks against running containers in Kubernetes environments or static Docker images from a registry or stored locally. The tool executes automated scans against specific STIG Security Guide (SSG) policies. The program will output either a JSON report with a summary of STIG check results for runtime checks or XCCDF XML and OpenSCAP XML and HTML for static checks. 

The static functionality includes the following profiles:

* Ubuntu 20.04 (ubuntu2004)
* Ubuntu 22.04 (ubuntu2204)
* Ubuntu 24.04 (ubuntu2404)
* Universal Base Image 8 (ubi8) - This runs the full RHEL 8 STIG
* Universal Base Image 9 (ubi9) - This runs the full RHEL 9 STIG
* Postgres 9 (postgres9)
* Apache Tommcat 9 (apache-tomcat9)
* Crunchy PostgreSQL (crunchy-postgresql)
* JBOSS (jboss)
* Java Runtime Environment 7 (jre7)
* MongoDB Enterprise (mongodb)
* nginx (nginx)

## Getting Started

### Dependencies

#### Overall
* `python3 >= 3.8 with pip installed`
* `saf`
* `CINC Auditor` - There is an option to install this tool after running the tool, but installing it manually is the most reliable.

#### Static
* `docker` - the Docker daemon must be running. If the target images are located in a private registry, you can be logged in to pull those images or pass credentials to the registry while using the tool.

### Install

* Run `pip install anchorestig-static`

### Install Dependencies

Anchore STIG requires, at a bare minimum, CINC auditor and SAF cli to function properly. For Runtime to function, the k8s plugin for CINC auditor must be installed as well. Anchore STIG has a function to assist with installing all of these tools. Below are the instructions for installing each of these.

* CINC auditor can be installed by running `anchorestig provision --install` or `anchorestig provision --install --privileged` for systems that require root. It also can be installed manually by running `curl -L https://omnitruck.cinc.sh/install.sh | bash -s -- -P cinc-auditor -v 5.22.50` or `curl -L https://omnitruck.cinc.sh/install.sh | sudo bash -s -- -P cinc-auditor -v 5.22.50` for systems that require root.
* The SAF cli can be installed in a few ways. When running static STIG like `anchorestig static TARGET_IMAGE` without saf installed, an interactive message will pop up to help install the tool. To install it manually, please follow the instructions [here](https://github.com/mitre/saf?tab=readme-ov-file#installation-1) to install it with either npm or homebrew. Please note that it must be installed locally. Using the Docker functionality will not work with Anchore STIG.

### Running the Program

#### Static

* Run the tool using `anchorestig static IMAGE`. 
    * Ex: `anchorestig static docker.io/ubi8:latest`
    * NOTE: please note that the first run will require ingesting the profile provided by the Anchore team. This can be accomplished with the `-t` flag pointed at the tarred policy file. Ex. `anchorestig static redhat/ubi8:latest -t ./policies.tar.gz`

```
Options:
  -u, --username TEXT        Username for private registry
  -p, --password TEXT        Password for private registry
  -r, --url TEXT             URL for private registry
  -b, --aws-bucket TEXT      S3 upload. Specify bucket name
  -a, --account TEXT         Anchore STIG UI account. Required for S3 upload
  -s, --insecure             Allow insecure registries or registries with
                             custom certs
  -l, --profile TEXT         Specify profile to run. Can be the name of an
                             existing profile or the path to a custom profile
  -i, --input-file TEXT      Specify the path to a custom input file to run
                             with a profile.
  -y, --sync                 Sync policies from Anchore
  -t, --sync-from-file TEXT  Sync policies from tar file provided by Anchore.
                             Provide the path to the tar file.
  --help                     Show this message and exit.
```

##### Viewing Results

Navigate to the `./stig-results` directory. The output directory containing output files will be named according to the image scanned.

## Help

Use the `--help` flag to see more information on how to run the program:

`anchorestig --help`

## Authors

* Sean Fazenbaker 
[@bakenfazer](https://github.com/bakenfazer)
* Michael Simmons 
[@MSimmons7](https://github.com/MSimmons7)

<!-- ## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the Anchore License - see the LICENSE.md file for details -->