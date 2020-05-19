import os
import json
import math

from datetime import datetime

from modules.emails.generateEmail import gen_emails
from modules.inbound_browsing.genInboundTraffic import gen_inbound_traffic
from modules.outbound_browsing.genOutboundTraffic import gen_browsing
from modules.outbound_browsing.genOutboundTraffic import click_links
from modules.malware.make_malware import make_malware

from utils import *

import argparse

#============================================
# Handle arguments for the script
#============================================
parser = argparse.ArgumentParser(description='')
parser.add_argument(
    '--level', '-l', type=int, default=10,
                    help='Difficulty level of the challenge. This determines the quantity of logs generated \
                         an the complexity of concepts that are tested.')
parser.add_argument(
    '--config_path', type=str, default="config/changeme/default/",
                    help='Use a custom config. Path to config containing employee and malicous config.\
                          Defaults to config/changeme/default')
parser.add_argument("--simulate", "-s", default=False, action='store_true', 
                    help="Run a simulation and provide a random config.")

args = parser.parse_args()
#============================================
# Most important part !!!!
# Display ascii art
#============================================
show_ascii_art()


#============================================
# Default Args
#============================================
level = args.level
# Number of emails to generate
EMAIL_COUNT = 50 * level#1000
# Number of generic web events to create
WEB_BROWSING_COUNT = 50 * level#1000
# Number of malicious emails to add in
MALICIOUS_EMAIL_COUNT = level
# Rate at which emails are blocked. The higher the difficulty, the higher the rate
EMAIL_BLOCK_RATE = math.log(level) / 10.0
# Number of malware samples to generate
MALWARE_COUNT =  int(level/2)


#============================================
# Set up all the configs
#============================================

if args.simulate:
    from simulator import run_simulation
    config_path = run_simulation(level=level)
else:
    config_path = args.config_path

# set up and metadata functions
set_up_output_dir('output')

start_time = datetime(2020, 6, 29, 8, 00, 00)

# load up the company's employees
company_info_config = os.path.join(config_path, "company.json")
with open(company_info_config, 'r') as f:
    company_info = json.loads(f.read())
        
# config for the adversary data
malicious_config = os.path.join(config_path, "malicious.json")
with open(malicious_config, 'r') as f:
    mal_config = json.loads(f.read())

## Creating a dictionary so we can pass global configs
## To other modules using kwargs without reloading them
config = {
    "company_info": company_info,
    "company_domain": "".join(company_info["company_name"].split(" ")).lower() + ".com",
    "hosts": company_info["employees"],
    "mal_config": mal_config,
    "start_time": start_time,
    "config_path": config_path,
    "output_path": 'output'
}


#============================================
# Main: here is all the action
#============================================
make_questions(**config)
add_employee_data(**config)

## Make Inbound traffic to the web server
gen_inbound_traffic(**config)
emails = gen_emails(count=EMAIL_COUNT, malicious_emails=MALICIOUS_EMAIL_COUNT, block_rate=EMAIL_BLOCK_RATE, **config)
### Make generic outbound web traffic
browsing_noise = gen_browsing(count=WEB_BROWSING_COUNT, **config)
### Get outbound  traffic from user clicking links emails
click_traffic = click_links(emails, CLICK_RATE=1, **config)

### Add traffic from emails to the noise.
### Write all this to file
all_outbound_traffic = click_traffic + browsing_noise
all_outbound_traffic.sort()
list_to_file(all_outbound_traffic, 'output/outbound_proxy_traffic.txt')


# generate the malware files
make_malware(MALWARE_COUNT)
