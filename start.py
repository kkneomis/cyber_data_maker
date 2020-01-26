import os
import random

from jinja2 import Template
from datetime import datetime
from datetime import timedelta

from utils import *
from emails.make_mail import gen_email_log
from emails.make_mail import create_email_obj


maker_config = load_json_config("config.json")
employees = maker_config.config["employees"]
date_time = datetime(1988, 6, 29, 8, 00, 00)


# load up the company's employees
with open('config/employees.json') as f:
    hosts = json.loads(f.read())
    
# load up the fake email senders
with open('config/general/names.txt') as f:
    sender_names = f.readlines()
    
with open('config/general/domains.txt') as f:
    sender_domains = f.readlines()

with open('config/general/script_censored.txt') as f:
    corpus  = f.read()

with open('config/general/templates/email_jinja_template.txt') as f:
    template_text = f.read()

template_obj = Template(template_text)


def gen_email_addr():    
    name = random.choice(sender_names).lower().strip().replace(" ", ".")
    domain = random.choice(sender_domains).strip()
    return "%s@%s"% (name, domain)


def gen_emails(num=3):
    """Generate fake emails"""
    mail_log = []
    output_path = maker_config.config["output_dir"]

    email_log_filename = os.path.join(output_path, "emails", "mail_logs.json")
    email_file_dir = os.path.join(output_path, "emails", "files")
    # create the email output directory if it doesn't already exist
    if not os.path.exists(email_file_dir):
        os.makedirs(email_file_dir)

    for i in range(num):
        sender = gen_email_addr()
        recipient = random.choice(hosts)["email_addr"]
        result = gen_email_log(date_time, sender_domains, sender, recipient, corpus)
        mail_log.append(result)
        
        # write the email to file
        with open(email_log_filename, 'a') as f:
            f.write(json.dumps(result))

    for email in mail_log:
        if email['result'] != "Blocked":
            create_email_obj(email, corpus, template_obj, email_file_dir)

    

    

def gen_browsing():
    """Generate fake web browsing traffic"""
    pass

def gen_web_server_data():
    """Generate web server logs"""
    pass

def inject_malicious_emails():
    """Generate emails from malicious senders"""
    pass

def inject_malicious_traffic():
    """General traffic of users clicking bad links"""
    pass


gen_emails()