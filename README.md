# Q Manager
This is the beta version of Torque based PBS job tracker with a locally hosted front-end viewer.
 
## Installation

This tool only needs Flask and pandas python pacakge which can be installed this way:
```bash
pip install flask pandas
```
## Usage

This tool is currently developed for the use of the [Torque](http://www.adaptivecomputing.com/products/open-source/torque/) based PBS job scheduler. It can be used to track the job-id and experiment parameters. In order to use this tool, you need to have a local copy of the job script and the experiment parameters. Then you can run the tool by:
```bash
python3 submitter.py
```
This will record the experiment parameters inside a csv file called `experiment_log.csv` and submit the job with the provided parameters. The job-id will be recorded too. In order to view the job status, you can run the following command:
```bash
python3 viewer.py
```
This will start a local server on port 5000. You can view the job status by visiting `localhost:5000` on your browser.

## To Do
- [ ] Add a feature to view the job status by job-id 
- [ ] Add timestamp field instead of output file name

## License
[MIT](https://choosealicense.com/licenses/mit/)
