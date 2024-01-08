from flask import Flask, render_template_string
import pandas as pd
import subprocess
import time
app = Flask(__name__)

def status_check(job_id):
    """
    Check the status of a job in the cluster
    :param job_id: job id
    :return: job status
    """
    # define the command to check the status of a job
    qstat_command = f"qstat -u erfan"
    # submit the command to the command line
    process = subprocess.run(qstat_command, capture_output=True, shell=True)

    # process = subprocess.Popen(qstat_command, stdout=subprocess.PIPE)
    # job_status, error = process.communicate()
    job_status = process.stdout.decode()
    # extract job_id field
    job_status = job_status.splitlines()
    job_status = job_status[2:]
    job_id_ = [job.split()[0] for job in job_status]
    print(f"list of jobs : {job_id_}, job id: {job_id}")
    job_id = f'{job_id}'
    # check if the job_id  is in the job_id_ list
    if job_id in job_id_:
        # only print the job status of the job_id
        job_status = [job for job in job_status if job_id in job]
        # extract the job status field
        job_status = [job.split()[4] for job in job_status]
        print(job_status)
    else:
        print(f"Job {job_id} is not in the queue")
        job_status = 'f'
    return job_status

@app.route('/')
def home():
    # Read the CSV file
    df = pd.read_csv('experiment_log.csv')
    # remove brackets from the entries
    df = df.replace({'\[': '', '\]': ''}, regex=True)
    # remove quotes from the entries
    df = df.replace({'\'': ''}, regex=True)
    # convrt the last column to a clickable link
    print(df['link'])
    raw_link = df['link']
    df['link'] = df['link'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')

    # Convert the DataFrame to HTML
    table = df.to_html(escape=False)

    # Create a simple HTML template
    template = """
    <html>
        <head>
            <title>Job Manager</title>
            <style>
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
        </style>
        </head>
        <body>
            <h1>Jobs</h1>
            {{ table|safe }}
        </body>
    </html>
    """
    # run the status check for each job every time the page is refreshed
    for i in range(len(df)):
        job_id = df['job_id'][i]
        print(job_id)
        job_status = status_check(job_id)
        print(job_status)
        # update the status of the job in the dataframe
        df['job_status'][i] = job_status
        print(df['job_status'][i])
    # remove the link formatting from the df['link'] column
    df['link'] = raw_link
    # write the updated dataframe to the csv file
    df.to_csv('experiment_log.csv', index=False)
    # Render the template with the table
    return render_template_string(template, table=table)

if __name__ == '__main__':
    app.run(debug=True)
