# Step 2: Submit Jobs

Distributed-FIJI batches jobs by plate so no matter how large your list of plates to process, each EC2 instance will process one job = one plate.
Once your job file is configured, simply use `python run.py submitJob files/{YourJobFile}.json` to send all the jobs to the SQS queue [specified in your config file](step_1_configuration.md).

## Configuring your job file

* **output_file_location:** The path of the output_file_location is relative to the root of your S3 bucket.
(e.g. `projects/output/`)
* **shared_metadata:**  Dictionary of metadata shared between all jobs.
Necessary metadata will depend upon the specific script you are running in FIJI.
(e.g. `{"input_file_location":"/home/ubuntu/bucket/projects/input","image_size":"1024","rows":"2","columns":"2"}`)
* **groups:** Dictionary of metadata specific to each job.
Each group is tasks that will be run in parallel.
(e.g `{"Well": "A1", "Plate":"Plate_1"}`)
