# Constants (User configurable)

APP_NAME = 'DistributedFiji'                # Used to generate derivative names unique to the application.
LOG_GROUP_NAME = APP_NAME 

# DOCKER REGISTRY INFORMATION:
DOCKERHUB_TAG = 'cellprofiler/distributed-fiji:latest'

# AWS GENERAL SETTINGS:
AWS_REGION = 'us-east-1'
AWS_PROFILE = 'default'                 # The same profile used by your AWS CLI installation
SSH_KEY_NAME = 'your-key-file.pem'      # Expected to be in ~/.ssh
AWS_BUCKET = 'your-bucket-name'

# EC2 AND ECS INFORMATION:
ECS_CLUSTER = 'default'
CLUSTER_MACHINES = 3
TASKS_PER_MACHINE = 1
MACHINE_TYPE = ['m4.xlarge']
MACHINE_PRICE = 0.10
EBS_VOL_SIZE = 30                       # In GB.  Minimum allowed is 22.
DOWNLOAD_FILES = 'False'

# DOCKER INSTANCE RUNNING ENVIRONMENT:
MEMORY = 4096                           # Memory assigned to the docker container in MB
SCRIPT_DOWNLOAD_URL = 'https://some/url/with/a/script.y'

# SQS QUEUE INFORMATION:
SQS_QUEUE_NAME = APP_NAME + 'Queue'
SQS_MESSAGE_VISIBILITY = 1*60           # Timeout (secs) for messages in flight (average time to be processed)
SQS_DEAD_LETTER_QUEUE = 'user_DeadMessages'

# MONITORING
AUTO_MONITOR = 'True'

# CLOUDWATCH DASHBOARD CREATION
CREATE_DASHBOARD = 'True'           # Create a dashboard in Cloudwatch for run
CLEAN_DASHBOARD = 'True'            # Automatically remove dashboard at end of run with Monitor

# REDUNDANCY CHECKS
EXPECTED_NUMBER_FILES = 7    #What is the number of files that trigger skipping a job?
MIN_FILE_SIZE_BYTES = 1      #What is the minimal number of bytes an object should be to "count"?
NECESSARY_STRING = ''        #Is there any string that should be in the file name to "count"?
