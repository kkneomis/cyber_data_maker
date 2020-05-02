import os
import json

from datetime import datetime
from tqdm import tqdm

from modules.emails.generateEmail import gen_emails
from modules.inbound_browsing.genInboundTraffic import gen_inbound_traffic
from modules.outbound_browsing.genOutboundTraffic import gen_browsing
from modules.outbound_browsing.genOutboundTraffic import click_links
from utils import *

import argparse

#============================================
# Handle arguments for the script
#============================================
parser = argparse.ArgumentParser(description='')
parser.add_argument(
    '--config_path', type=str, default="config/changeme/default/",
                    help='Use a custom config. Path to config containing employee and malicous config.\
                          Defaults to config/changeme/default')
parser.add_argument("--simulate", "-s", default=False, action='store_true', help="Run a simulation and provide a random config.")


#============================================
# Set up all the configs
# TODO: find a way to share with with modules
#============================================
args = parser.parse_args()
if args.simulate:
    from simulator import run_simulation
    config_path = run_simulation()
else:
    config_path = args.config_path

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


# set up and metada functions
set_up_output_dir('output')
make_questions(**config)
add_employee_data(**config)

## Make Inbound traffic to the web server
gen_inbound_traffic(**config)
emails = gen_emails(count=1000, **config)
### Make generic outbound web traffic
browsing_noise = gen_browsing(count=1000, **config)
### Get outbound  traffic from user clicking links emails
click_traffic = click_links(emails, **config)

### Add traffic from emails to the noise.
### Write all this to file
all_outbound_traffic = click_traffic + browsing_noise
all_outbound_traffic.sort()
list_to_file(all_outbound_traffic, 'output/outbound_proxy_traffic.txt')

