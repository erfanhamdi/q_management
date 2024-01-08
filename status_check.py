def status_check(job_id):
    """
    Check the status of a job in the cluster
    :param job_id: job id
    :return: job status
    """
    # define the command to check the status of a job
    qstat_command = f"qstat -j {job_id}"
    # submit the command to the command line
    process = subprocess.Popen(qstat_command, stdout=subprocess.PIPE)
    job_status, error = process.communicate()
    # parse job status and extract the state of the job
    job_status = job_status.decode()
    job_status = job_status.splitlines()
    job_status = [line for line in job_status if "job_state" in line]
    job_status = job_status[0].split()[2]
    return job_status
job_id = '3530317'
qstat_command = f"qstat -u erfan"
# submit the command to the command line
process = subprocess.run(qstat_command, capture_output=True, shell=True)

# process = subprocess.Popen(qstat_command, stdout=subprocess.PIPE)
# job_status, error = process.communicate()
job_status = process.stdout.decode()
# parse job status and extract the state of the job
job_status = job_status.splitlines()
job_status = job_status[2:]
job_status = [job.split()[4] for job in job_status]