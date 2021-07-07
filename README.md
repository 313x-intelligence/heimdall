# Heimdall Cloud Checker

<img align="right" height="300" width="370" src="https://user-images.githubusercontent.com/6532445/124816083-7642fc80-df3e-11eb-8b43-e59216187730.png" alt="Visius Heimdall Logo">

## About
[Visius](https://visius.io)  is a Brazilian cybersecurity startup that follows the signs of the [crimson thunder ;)](https://www.youtube.com/watch?v=SMkMp0oAL7E) :guitar:!

As we value open source initiatives a lot we've decided to open Heimdall for everyone to see and help us to secure our digital life.
> "Be warned, I will honor my sworn oath to protect this realm as its gatekeeper. If your return threatens the safety of Asgard, Bifrost will remain closed and you will be left to die on the cold waste of Jotunheim."


Heimdall is a tool to check for risks on your AWS.

## Running

Prerequisites:

- Python3

### On Linux

Download this project, extract it to a folder and navigate to it.

(Optional) Create and run a python virtual environment: `python -m venv .venv && source .venv/bin/activate`

Install boto3 module: `pip install boto3`

Run: `python main.py`

### Options

- none : check everything
- -h | --help : Show help
- -c | --crypto : Checks if Encryption is enabled
- -i | --credentials : Checks for password policy and users MFA
- -e | --exposed : Checks for exposed items
- -l | --logs : Checks for active Logs


### To do
- Add support to Azure
- Add support to GCP
- Any other cool stuff

## Sponsor

The very first Viking Startup, Visius <img src='https://user-images.githubusercontent.com/6532445/124814004-de441380-df3b-11eb-918b-5541936155be.png'  width="35" height="20">
