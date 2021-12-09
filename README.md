# Dirstatstocloudwatch

Dirstatstocloudwatch is a quick and dirty way to get basic stats (number of objects, and total size) out to AWS CloudWatch. 

It is designed to be run via cron on a local system. It can optionally be run in a docker container, but note that you'll have to manually configure the docker container to have access to the directories that you wish to monitor.

## Configuring AWS permissions for this tool:

This tool uses boto3 (https://aws.amazon.com/sdk-for-python/) python bindings to access AWS. A full discussion of how to authenticate with boto3 and how to authenticate with boto3 is outside the scope of this document. For the sake of example, we will define environment variables, but that is not necessarily the best or most secure method in your environment (and probably isn't).

To run an example, you should define a role with minimal permissions. For a simple example, create a user in AWS and assign them that role. Generate an IAM access key for that user. Save the AWS_ACCESS_KEY_ID and AWS_SECRET_KEY somewhere safe.


Here's a sample role:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "cloudwatch:PutMetricData",
            "Resource": "*"
        }
    ]
}
```

### Running a simple example from the console

Before doing this, create a virtual environment using your choice of virtual environment tools, otherwise you'll be installing the dependencies in your base python install, which isn't ideal.

```zsh -
git clone your-repo
cd code/dirstatstocloudwatch
pip3 install -r requirements.txt
```

Declare your environment variables for AWS
```zsh -
export AWS_ACCESS_KEY_ID=YOURACCESSKEY
export AWS_SECRET_ACCESS_KEY=YOURSECRETKEY
export AWS_DEFAULT_REGION=us-east-1
```

Run the tool:
``` zsh - 
python3 dirstatstocloudwatch/main.py -c=config/sample-config.yaml
```

### Running the tool with Docker:


You'll need to add mounts to docker for the folder(s) you want to monitor.
You could also use a mount to point to an external config file if you'd prefer to not have to rebuild the container every time you change the config file.

First, install docker on your platform.

Build the image:
```zsh
docker build -t dirstatstocloudwatch .
```

Run the image:
```zsh
docker run -e AWS_DEFAULT_REGION=us-east-1 \ 
           -e AWS_ACCESS_KEY_ID=XX \
           -e AWS_SECRET_ACCESS_KEY='XX' \
           -v /path/to/local/fold:/path/in/container \
           dirstatstocloudwatch \
           -c=/dirstatstocloudwatch/config/sample-config.yaml
```

Don't forget to prune old containers if you run it this way. 

Another option for running in docker if you don't want to generate a new container on every run is to create the container, then start it.
This is the recommended way to run as a container, especially if you're going to be triggering it often via cron:
```zsh
docker create --name dirstatstocloudwatch_prod \
                    -e AWS_DEFAULT_REGION=us-east-1 \
                    -e AWS_ACCESS_KEY_ID=XX \
                    -e AWS_SECRET_ACCESS_KEY='XX' 
                    -v /path/to/local/fold:/path/in/container \
                    dirstatstocloudwatch \
                    -c=/dirstatstocloudwatch/config/sample-config.yaml

docker start dirstatstocloudwatch_prod
```

FUTURE TODO:
* Optimize gathering of stats for speed
* document config file, possible optimize config file format to condense it
* cleanup loglevels for debug
* add loglevels to config file
