# run a command in the command line
import os
import sys
import subprocess
import time
import datetime


command = "qsub submit_job.sh"
for jobs in range(1):

    # time stamp based output folder
    param_dict = {
                'l_0': [0.004],
                'delta_T_1':[0.00001],
                'delta_T_2':[0.00001],
                'stag_iter': [5],
                'loading':['shear'],
                'Young': [210e3],
                'Poisson': [0.3],
                'G_c': [2.7],
                'num_steps': [4000],
                'mesh_add':['meshes/miehe_regional_0.xml'],
                'description': ['miehe_regional_0'],
                'f_y': [2445.42],
                'tol': [1e-4],
                'ambati': [False],
                'isotropic': [False],

                }
    time_stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
    output_folder = f'results/{time_stamp}'
    param_dict['output_add'] = [output_folder]
    # create the output folder if it does not exist already
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    # create a yaml template file containing the key value pairs
    with open('material.yaml', 'w') as f:
        for key, value in param_dict.items():
            f.write(f'{key}: {value[0]}\n')
    # append to the experiment log file the parameters
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    # get the last line of the output
    output = output.splitlines()[-1]
    job_id = output.split()[2]
    # convert the job id to a string
    job_id = str(job_id, 'utf-8')
    print(output)
    print(f"job id is {job_id}")
    # create a header list contining the job_id and the parameters keys
    header = ['job_id']
    header.extend(param_dict.keys())
    # create a values list containing the job_id and the parameters values
    values = [job_id]
    # update the output_folder parameter
    param_dict['link'] = [f'https://scc-ondemand1.bu.edu/pun/sys/dashboard/files/fs//projectnb/lejlab2/erfan/Recode/{output_folder}']
    values.extend(param_dict.values())
    # create or append to the experiment log file
    with open('experiment_log.csv', 'a') as f:
        # if the file is empty write the header
        if os.stat('experiment_log.csv').st_size == 0:
            f.write(','.join(header) + '\n')
        # write the values
        f.write(','.join(map(str, values)) + '\n')
    # open the material.yaml file and change the parameters
    # write the changes to the file
    job_status = 'q'
    # while job_status != 'r':
    #     print(job_status)
    # # check job status
    #     qstat_command = f"qstat -u erfan; awk '/{job_id}/ {{print $5}}'"
    #     # submit the command to the command line
    #     process = subprocess.run(qstat_command, capture_output=True, shell=True)

    #     # process = subprocess.Popen(qstat_command, stdout=subprocess.PIPE)
    #     # job_status, error = process.communicate()
    #     job_status = process.stdout.decode()
    #     print(f"job status is {job_status}")
    #     print(f"error is {error}")
    #     # # job_status = os.system(f"qstat -u erfan | awk '/{job_id}/ {{print $5}}'")
    #     # pause for 30 seconds
    #     # print(job_status)
    #     # wait for 10 seconds
    #     time.sleep(30)

