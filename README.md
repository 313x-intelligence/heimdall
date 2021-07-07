Visius Heimdall is a tool to check for risks on your AWS.

# Running

Prerequisites:

- Python3

## On Linux

Download this project, extract it to a folder and navigate to it.

(Optional) Create and run a python virtual environment: `python -m venv .venv && source .venv/bin/activate`

Install boto3 module: `pip install boto3`

Run: `python main.py`

## Options

- none : check everything
- -h | --help : Show help
- -c | --crypto : Checks if Encryption is enabled
- -i | --credentials : Checks for password policy and users MFA
- -e | --exposed : Checks for exposed items
- -l | --logs : Checks for active Logs

# Sponsor

Visius Logo
