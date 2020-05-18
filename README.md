# Cyber Challenge Data Maker

## TF is this thing?

Cyber Data Maker is a framework for creating gamified data to help cybersecurity students learn
how to parse through log data to analyze network intrusions. It can help students improve their bash-fu and learn how to pivot.

It shows students that playing defense is actually pretty fun!

# What you get:

* A bundle of data containing:
  * A list of company employees
  * Mail logs
  * Email files for the accepted emails
  * Outbound web logs (from employee browsing)
  * Some malware to deofuscate
* A set of questions for students to answer

```simeonkakpovi@urpwned-com:~/Documents/cyber/Dev/challenge_maker/output$ tree
.
├── emails
│   ├── email_00a78670392a6998efaac185eeabe896664153e0
│   ├── email_039be9d87854bdcf5fe63cd9afa22fef3daae529
│   ├── ...
├── employees.json
├── inbound_proxy_traffic.txt
├── mail_logs.json
├── malware
│   └── 1_dac0cac70c0f56bafa3aa26abba348066a3dea6c
├── outbound_proxy_traffic.txt
└── prompt.txt
```


So far, there is only one scenario and it goes like this:
An adversary sends malicious emails to the employees of a company. Some of the employees click on the emails. Malware is delivered to those employees. 

All events in the scenario can be found in the provided logs. In addition, the timestamps of events should match.



## Setting Up

Modify the config files in `config/changeme` to reflect your desired storyline. 

`employees.json` reflects the names, IPs and email addresses of the employees in your fictional organization.

`malicious.json` contains information about the fictional hacker and their infrastructure. 

`corpus.txt` is the text base used generate the ficticious emails. This can be any long piece of text. 

It is your responsibility to make sure that the story makes sense at the end of the day. 


## Getting Started

Run the start file to get started

```
$ python run_modules.py
```

The resulting data will be in the `output/` folder

## Simulator

You also have the option of using the simulator script to create storyline for you.
This script will generate a "random" company with employees and "random" adversary data.
```bash
$ python run_modules.py -s
```

Alternatively you can make your own config and tell the challenge make to use that.
```
python run_modules.py --config config/changeme/simulated/
```
## Levels

You can adjust the difficulty of the challenge using the `--level` flag. Where 1 is the minimum and the sky is the limit. The leveling system is still a work in progress


### TODO

* Add malicious activity to inbound web data
* Add in option for different compromise scenarios
* Create host log module (starting with MFT)
