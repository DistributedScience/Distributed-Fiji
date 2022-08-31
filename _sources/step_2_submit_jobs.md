# Step 2: Submit Jobs

Distributed-Fiji works to run a Fiji script you've designed across many sets of images all in parallel.
The specifics of your script will determine specifically how your larger image set is broken down - is your script designed to work on one site, one well, one movie, one plate?
Each complete set of images required to run your script we refer to as one job.
Once you've determined what groups of images you have to process, you're ready to start configuring your job file.
Once your job file is configured, simply use `python run.py submitJob files/{YourJobFile}.json` to send all the jobs to the SQS queue [specified in your config file](step_1_configuration.md).

## Configuring your job file

* **output_file_location:** The location where your files will be output.
The path of the output_file_location is relative to the root of your S3 bucket.
(e.g. `projects/output/`)
* **shared_metadata:**  Dictionary of metadata shared between all jobs.
Necessary metadata will depend upon the specific script you are running in FIJI.
If the location of input data is on your bucket and is passed to the script, make sure you pass a file location starting with /home/ubuntu/bucket.
(e.g. `{"input_file_location":"/home/ubuntu/bucket/projects/input","image_size":"1024","rows":"2","columns":"2"}`)
* **groups:** Dictionary of metadata specific to each job.
Each group is tasks that will be run in parallel with other groups.
(e.g `{"Well": "A1", "Plate":"Plate_1"}`)
