# ec2instance

ec2instance is the "docker run -it" of AWS EC2. It is a single command that very quickly launches an EC2 instance from
the CLI and takes care of the legwork to make it immediately usable for you.

## Demo

[![asciicast](https://asciinema.org/a/458558.svg)](https://asciinema.org/a/458558?autoplay=1)

## Install

```
pip install ec2instance
```

## Usage

```
usage: ec2instance [-h] [-t INSTANCE_TYPE] [-i AMI_IDENTIFIER] [-f USER_DATA_FILENAME]
                   [--volume-size VOLUME_SIZE] [--profile PROFILE_NAME] [--region AWS_REGION] [-d]
                   [--show-data-path]

Quickly launch an EC2 instance for small tasks. The instance's lifecycle is tied to the process,
enabling easy Ctrl+C instance termination when done.

options:
  -h, --help            show this help message and exit
  -t, --type INSTANCE_TYPE
                        EC2 instance type. (default: t3a.micro)
  -i, --ami AMI_IDENTIFIER
                        EC2 AMI id. You may also pass "ubuntu" as a shortcut to get the latest
                        Ubuntu LTS, or "amazonlinux" as a shortcut to get the latest Amazon Linux.
                        (default: ubuntu)
  -f, --user-data USER_DATA_FILENAME
                        EC2 "user data" script. Path to a shell script. AWS will upload and run
                        this script on the instance immediately after launch. (default:
                        ~/.config/ec2instance_cmd/user_data_scripts/default.sh)
  --volume-size VOLUME_SIZE
                        Root EBS volume size (GiB). (default is normally approximately 8GiB)
  --profile PROFILE_NAME
                        AWS credentials profile name to use.
  --region AWS_REGION   Specific AWS region to use.
  -d, --detach, --non-interactive, --json
                        By default an interactive shell will be opened in the spawned instance,
                        and the instance will be terminated when the shell is closed. To instead
                        output ec2 metadata as json and then detach, specify --detach.
  --show-data-path      Print out the path where ec2instance is storing local data and
                        configuration.

help & support:
  https://github.com/personalcomputer/ec2instance/issues
```

## Notes

- Before using ec2instance, you must configure AdministratorAccess-level AWS authentication credentials locally:
  - 1.) [install awscli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
  - 2.) Run `aws configure` and enter in your AWS access key. How to get an AWS access key is not in scope of this
    guide.
- Upon running ec2instance for the first time, it will tell you it is automatically creating a tiny sandbox in your AWS
  account to ensure that there are no possible conflicts or security concerns from using ec2instance. This sandbox
  consists of generating a dedicated fresh VPC and SSH keypair, and these are persisted between invocations of
  ec2instance. There is no AWS fee associated with these resources, and their auto-generated names are obvious and
  logged to console. Feel free to delete them if you stop using ec2instance.
