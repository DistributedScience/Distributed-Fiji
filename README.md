# Distributed-FIJI
Run encapsulated docker containers with FIJI in the Amazon Web Services infrastructure.

This code is an example of how to use AWS distributed infrastructure for running FIJI.
The configuration of the AWS resources is done using boto3 and the awscli. The worker is written in Python 
and is encapsulated in a docker container. There are four AWS components that are needed to run 
distributed jobs:

1. An SQS queue
2. An ECS cluster
3. An S3 bucket
4. A spot fleet of EC2 instances

All of them can be managed through the AWS Management Console. However, this code helps to get
started quickly and run a job autonomously if all the configuration is correct. The code runs a
script that links all these components and prepares the infrastructure to run a distributed 
job. When the job is completed, the code is also able to stop resources and clean up components. It also adds logging and alarms via CloudWatch, helping the user troubleshoot runs and destroy stuck machines.

## Running the code

### Step 1
Edit the config.py file with all the relevant information for your job. Then, start creating 
the basic AWS resources by running the following script:

 $ python run.py setup

This script intializes the resources in AWS. Notice that the docker registry is built separately,
and you can modify the worker code to build your own. Anytime you modify the worker code, you need
to update the docker registry using the Makefile script inside the worker directory.

### Step 2
After the first script runs successfully, the job can now be submitted to AWS using the following command:

 $ python run.py submitJob files/exampleJob.json
 
Running the script uploads the tasks that are configured in the json file. This assumes that your 
data is stored in S3, and the json file has the paths to find input and output directories. You have to 
customize the exampleJob.json file with paths that make sense for your project. 
Each job will be run in parallel - you define each task in your input file to guide the parallelization.

### Step 3
After submitting the job to the queue, we can add computing power to process all tasks in AWS. This
code starts a fleet of spot EC2 instances which will run the worker code. The worker code is encapsulated
in docker containers, and the code uses ECS services to inject them in EC2. All this is automated
with the following command:

 $ python run.py startCluster files/exampleFleet.json

After the cluster is ready, the code informs you that everything is setup, and saves the spot fleet identifier 
in a file for further reference.

### Step 4
When the cluster is up and running, you can monitor progress using the following command:

 $ python run.py monitor files/APP_NAMESpotFleetRequestId.json

The file APP_NAMESpotFleetRequestId.json is created after the cluster is setup in step 3. It is 
important to keep this monitor running if you want to automatically shutdown computing resources
when there are no more tasks in the queue (recommended).

See the wiki for more information about each step of the process.

![DistributedFiji](https://user-images.githubusercontent.com/6721515/148241479-d2601e3b-8c5f-4104-b0b8-446c533408e0.png)
