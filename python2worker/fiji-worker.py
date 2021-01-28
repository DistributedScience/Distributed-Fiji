from __future__ import print_function
import boto3
import glob
import json
import logging
import os
import re
import subprocess
import sys 
import time
import watchtower
import string

#################################
# CONSTANT PATHS IN THE CONTAINER
#################################

DATA_ROOT = '/home/ubuntu/bucket'
PLUGIN_DIR = '/home/ubuntu/CellProfiler-plugins'
QUEUE_URL = os.environ['SQS_QUEUE_URL']
AWS_BUCKET = os.environ['AWS_BUCKET']
LOG_GROUP_NAME= os.environ['LOG_GROUP_NAME']
EXPECTED_NUMBER_FILES= os.environ['EXPECTED_NUMBER_FILES']
if 'MIN_FILE_SIZE_BYTES' not in os.environ:
    MIN_FILE_SIZE_BYTES = 1
else:
    MIN_FILE_SIZE_BYTES = int(os.environ['MIN_FILE_SIZE_BYTES'])
if 'NECESSARY_STRING' not in os.environ:
    NECESSARY_STRING = False
else:
    NECESSARY_STRING = os.environ['NECESSARY_STRING']
if 'DOWNLOAD_FILES' not in os.environ:
    DOWNLOAD_FILES = False
else:
    DOWNLOAD_FILES = os.environ['DOWNLOAD_FILES']
SCRIPT_DOWNLOAD_URL = os.environ['SCRIPT_DOWNLOAD_URL']
SCRIPT_NAME = os.path.split(SCRIPT_DOWNLOAD_URL)[1]

localIn = '/home/ubuntu/local_input'


#################################
# CLASS TO HANDLE THE SQS QUEUE
#################################

class JobQueue():

    def __init__(self, queueURL):
        self.client = boto3.client('sqs')
        self.queueURL = queueURL
    
    def readMessage(self):
        response = self.client.receive_message(QueueUrl=self.queueURL, WaitTimeSeconds=20)
        if 'Messages' in response.keys():
            data = json.loads(response['Messages'][0]['Body'])
            handle = response['Messages'][0]['ReceiptHandle']
            return data, handle
        else:
            return None, None

    def deleteMessage(self, handle):
        self.client.delete_message(QueueUrl=self.queueURL, ReceiptHandle=handle)
        return

    def returnMessage(self, handle):
        self.client.change_message_visibility(QueueUrl=self.queueURL, ReceiptHandle=handle, VisibilityTimeout=60)
        return

#################################
# AUXILIARY FUNCTIONS
#################################


def monitorAndLog(process,logger):
    while True:
        output= process.stdout.readline()
        if output== '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
            logger.info(output)  

def printandlog(text,logger):
    print(text)
    logger.info(text)
	
def stringify_metadata_dict(mdict):
    met_string = ""
    for eachmeta in mdict.keys():
        met_string+=eachmeta+"='"+mdict[eachmeta]+"', "
    return met_string[:-2]

#################################
# RUN FIJI PROCESS
#################################

def runFIJI(message):
    #List the directories in the bucket- this prevents a strange s3fs error
    rootlist=os.listdir(DATA_ROOT)

    # Configure the logs
    logger = logging.getLogger(__name__)

    # Prepare paths and parameters
    localOut = 'output'
    remoteOut = message['output_file_location']

    # Start logging 
    metadataID = stringify_metadata_dict(message['Metadata'])
    metadata_for_log_name=metadataID.replace('*','.')
    watchtowerlogger=watchtower.CloudWatchLogHandler(log_group=LOG_GROUP_NAME, stream_name=metadataID,create_log_group=False)
    logger.addHandler(watchtowerlogger)	
	
    # Build and run CellProfiler command
    cmd = ["Fiji.app/ImageJ-linux64","--ij2", "--headless", "--console", "--run",os.path.join("Fiji.app/plugins",SCRIPT_NAME)]
    cmd.append(stringify_metadata_dict(message['shared_metadata']) + ', ' + metadataID)
    print('Running', cmd)
    logger.info(cmd)
    
    subp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    monitorAndLog(subp,logger)

    # Get the outputs and move them to S3
    # Figure out how many output files there were - thanks https://stackoverflow.com/a/29769297
    print('Checking output folder size')
    filenum = 0
    for _, _, filenames in os.walk(localOut):
            filenum += len(filenames)
    print(localOut,filenum)
    if filenum>=int(EXPECTED_NUMBER_FILES):
        mvtries=0
        while mvtries <3:
            try:
                printandlog('Move attempt #'+str(mvtries+1),logger)
                cmd = 'aws s3 mv ' + localOut + ' s3://' + AWS_BUCKET + '/' + remoteOut + ' --recursive'
                subp = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out,err = subp.communicate()
                printandlog('== OUT \n'+out, logger)
                if err == '':
                    break
                else:
                    printandlog('== ERR \n'+err,logger)
                    mvtries+=1
            except:
                printandlog('Move failed',logger)
                printandlog('== ERR \n'+err,logger)
                time.sleep(30)
                mvtries+=1
        if mvtries<3:
            printandlog('SUCCESS',logger)
            logger.removeHandler(watchtowerlogger)
            return 'SUCCESS'
    else:
        printandlog('OUTPUT PROBLEM. Only '+str(filenum)+' files detected. Giving up on '+metadataID,logger)
        logger.removeHandler(watchtowerlogger)
        return 'OUTPUT_PROBLEM'		
    
#################################
# MAIN WORKER LOOP
#################################

def main():
    queue = JobQueue(QUEUE_URL)
    # Main loop. Keep reading messages while they are available in SQS
    while True:
        msg, handle = queue.readMessage()
        if msg is not None:
            result = runFIJI(msg)
            if result == 'SUCCESS':
                print('Batch completed successfully.')
                queue.deleteMessage(handle)
            else:
                print('Returning message to the queue.')
                queue.returnMessage(handle)
        else:
            print('No messages in the queue')
            break

#################################
# MODULE ENTRY POINT
#################################

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print('Worker started')
    main()
    print('Worker finished')

