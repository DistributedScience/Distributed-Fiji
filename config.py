# Constants (User configurable)

APP_NAME = 'Distributed-DeepProfiler'                # Used to generate derivative names unique to the application.

# DOCKER REGISTRY INFORMATION:
DOCKERHUB_TAG = 'michaelbornholdt/deep_profiler:v2'

# AWS GENERAL SETTINGS:
AWS_REGION = 'us-east-1'
AWS_PROFILE = 'default'                 # The same profile used by your AWS CLI installation
SSH_KEY_NAME = 'jump_mbhornhol.pem'      # Expected to be in ~/.ssh
AWS_BUCKET = 'imaging-platform'

# EC2 AND ECS INFORMATION:
ECS_CLUSTER = 'default'
CLUSTER_MACHINES = 136
TASKS_PER_MACHINE = 1
MACHINE_TYPE = ['p2.xlarge']
MACHINE_PRICE = 0.9
EBS_VOL_SIZE = 60                     # In GB.  Minimum allowed is 22.
DOWNLOAD_FILES = 'False'

# DOCKER INSTANCE RUNNING ENVIRONMENT:
MEMORY = 6000                           # Memory assigned to the docker container in MB
SCRIPT_DOWNLOAD_URL = 'https://some/url/with/a/script.y'

# SQS QUEUE INFORMATION:
SQS_QUEUE_NAME = APP_NAME + 'Queue'
SQS_MESSAGE_VISIBILITY = 1*60           # Timeout (secs) for messages in flight (average time to be processed)
SQS_DEAD_LETTER_QUEUE = 'arn:aws:sqs:some-region:111111100000:DeadMessages'

# LOG GROUP INFORMATION:
LOG_GROUP_NAME = APP_NAME 

# REDUNDANCY CHECKS
EXPECTED_NUMBER_FILES = 7    #What is the number of files that trigger skipping a job?
MIN_FILE_SIZE_BYTES = 1      #What is the minimal number of bytes an object should be to "count"?
NECESSARY_STRING = ''        #Is there any string that should be in the file name to "count"?
