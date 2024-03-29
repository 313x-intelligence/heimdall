# Heimdall Cloud Checker :brazil:

<img align="right" height="300" width="370" src="https://user-images.githubusercontent.com/6532445/124816083-7642fc80-df3e-11eb-8b43-e59216187730.png" alt="Visius Heimdall Logo">

As we value open source initiatives a lot, we've decided to open Heimdall for everyone to see and help us to secure our digital life.
> "Be warned, I will honor my sworn oath to protect this realm as its gatekeeper. If your return threatens the safety of Asgard, Bifrost will remain closed and you will be left to die on the cold waste of Jotunheim."


Heimdall is a tool to check risks on your AWS.

## Running

Prerequisites:

- Python3
- Poetry
- Make
- Boto3

### On Linux

Download this project, extract it to a folder and navigate to it.

```python
git clone git@github.com:313x-intelligence/heimdall.git
make setup/dev
make start

# Format files before commit
make format/run
```

### Screenshots
![1](https://user-images.githubusercontent.com/67867099/125287076-e2cd4b00-e2f2-11eb-890f-889c0f294b59.jpeg)

![2](https://user-images.githubusercontent.com/67867099/125287099-e82a9580-e2f2-11eb-9234-5435941f2ed9.jpeg)

![3](https://user-images.githubusercontent.com/67867099/125287120-ec56b300-e2f2-11eb-8d46-3b9d13692abf.jpeg)

![4](https://user-images.githubusercontent.com/67867099/125287129-ef51a380-e2f2-11eb-8c3c-206246e34e3d.jpeg)


### Options
```
- none : check everything
- -h | --help : Show help
- -c | --crypto : Checks if Encryption is enabled
- -i | --credentials : Checks for password policy and users MFA
- -e | --exposed : Checks for exposed items
- -l | --logs : Checks for active Logs

