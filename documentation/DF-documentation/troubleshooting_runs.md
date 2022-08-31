# Troubleshooting


| SQS  | CloudWatch   |  S3 | EC2/ECS  | Problem  | Solution |
|---|---|---|---|---|---|
|   | Within a single log, your run command is logging multiple times. | Expected output seen. |   | A single job is being processed multiple times. | SQS_MESSAGE_VISIBILITY is set too short. See SQS-QUEUE-INFORMATION for more information. |
|   |   |   | Machines made in EC2 and dockers are made in ECS but the dockers are not placed on the machines. | There is a mismatch in your DS config file. |  Confirm that the MEMORY matches the MACHINE_TYPE  set in your config. |
