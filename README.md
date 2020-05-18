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




So far, there is only one scenario and it goes like this:
An adversary sends malicious emails to the employees of a company. Some of the employees click on the emails. Malware is delivered to those employees. 

All events in the scenario can be found in the provided logs. In addition, the timestamps of events should match.


## Example Challenge

One example prompt could be:

```
You are a cybersecurity analyst at Daily Bugle, The Daily Bugle is a media organization, which engages in creating, collecting, and distributing news and information. It includes newspapers, print, and digital products, and mobile applications..

Part 1

Question 1
Several users reported having received suspicious emails from twitterdevice@protonmail.com. Who did this sender send messages to?

Question 2
Some of these emails were blocked by your spam filters. Which of your employees actually received the messages?

Question 3
What domains were used in the links contained in these suspicious emails?

Question 4
Which IP addresses were asssociated with these links?

Question 5
Which users clicked on these links?

Question 6
Are there any other email senders associated with this activity? What are those email addresses?


Part 2

You were able to capture some of the malware that was downloaded by your users. 
They are obfuscated powershell scripts that attempt to download a new backdoor. 
You have been told to block the delivery urls before any more malware is downloaded.

You must identify the links to the 2nd stage malware samples by deobfuscating the files in the malware folder.
```


Example of the data structure:

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
