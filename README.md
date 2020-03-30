# Cyber Challenge Data Maker

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
challenge_maker$ python simulator.py 
New config at config/changeme/simulated/company.json
New config at config/changeme/simulated/malicious.json
```

When you do so, you must specfic the new config directory for the project to use
```
python run_modules.py --config config/changeme/simulated/
```

### TODO

* Fix malware module maker to work cross platform
* Add in inbound web data
* Add in option for different compromise scenarios