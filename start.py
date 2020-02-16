import os
import random

from jinja2 import Template
from datetime import datetime
from datetime import timedelta

from utils import *
from emails.make_mail import Email
from emails.make_mail import create_email_obj
from outbound_browsing.make_outbound_traffic import OutboundEvent


maker_config = load_json_config("config.json")
employees = maker_config.config["employees"]
date_time = datetime(2020, 6, 29, 8, 00, 00)





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

with open('config/general/external_hosts.txt', 'r') as f: 
    endpoints = f.readlines()

with open('config/general/malicious.json', 'r') as f: 
    mal_config = json.loads(f.read())

#template_obj = Template(template_text)
TEMPLATE_OBJ = Template(template_text)
MAIL_LOG = []
WEB_EVENTS = []

def gen_email_addr():    
    name = random.choice(sender_names).lower().strip().replace(" ", ".")
    domain = random.choice(sender_domains).strip()
    return "%s@%s"% (name, domain)

OUTPUT_PATH = maker_config.config["output_dir"]
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

def gen_emails(num=3):
    """
    Generate a log of background email activity 
    Emails are either accepted or blocked
    Generate email files for accepted emails the logs
    """
    
    
    # output dictories for the logs and email fiels
    email_log_filename = os.path.join(OUTPUT_PATH, "mail_logs.json")
    email_file_dir = os.path.join(OUTPUT_PATH, "emails", "files")

    # create the email output directory if it doesn't already exist
    if not os.path.exists(email_file_dir):
        os.makedirs(email_file_dir)

    # creating {num} number of emails and adding the mail log
    for i in range(num):
        sender = gen_email_addr()
        recipient = random.choice(hosts)["email_addr"]
        result = Email(date_time, sender_domains, sender, recipient, corpus).stringify()
        MAIL_LOG.append(result)
        
        # write the email to file
        with open(email_log_filename, 'a') as f:
            f.write(json.dumps(result))

    #print(json.dumps(MAIL_LOG))

    # generate email files
    for email in MAIL_LOG:
        # we are only generating files for accepted emails
        if email['result'] != "Blocked":
            create_email_obj(email, corpus, TEMPLATE_OBJ, email_file_dir)


def inject_malicious_emails():
    """Generate emails from malicious senders"""
    # creating {num} number of emails and adding the mail log

    sender = mal_config["sender"]
    for i in range(5):
        # generate blocked emails
        recipient = random.choice(hosts)["email_addr"]
        subject = random.choice(mal_config["blocked_subjects"])
        link = random.choice(mal_config["links"])["url"]
        new_mail = Email(date_time, sender_domains, sender, recipient, corpus, 
                        result="Blocked", subject=subject, link=link)
        MAIL_LOG.append(new_mail.stringify())
        

    for i in range(3):
        # generate accepted emails
        recipient = random.choice(hosts)["email_addr"]
        subject = random.choice(mal_config["accepted_subjects"])
        new_mail = Email(date_time, sender_domains, sender, recipient, corpus,
                             result="Accepted", subject=subject)
        MAIL_LOG.append(new_mail.stringify())



def gen_browsing(num):
    """Generate fake web browsing traffic"""
    
    for i in range(num):
        new_event = OutboundEvent(date_time, hosts, endpoints).stringify()
        WEB_EVENTS.append(new_event)
    
    
    


def inject_malicious_traffic():
    """General traffic of users clicking bad links"""

    def get_link_ip(url):
        """
        Search the config file for the 
        IP addr corresponding to a link
        """
        for link in mal_config["links"]:
            if link["url"] == url:
                return link["ip"]

    def get_user_from_email(email_addr):
        """
        Get full user info from config file 
        using the user's email addr
        """
        for user in hosts:
            if user["email_addr"] == email_addr:
                return user

    for event in MAIL_LOG:
        if event["link"]:
            user = get_user_from_email(event["recipient"])
            link = event["link"]
            domain = link.split("//")[-1].split("/")[0].split('?')[0]
            ip = get_link_ip(link)
            endpoint = "%s/ %s" % (domain, ip)
            new_event = OutboundEvent(date_time, hosts, endpoints, 
                                     user=user, endpoint=endpoint).stringify()
            WEB_EVENTS.append(new_event)


    print json.dumps(WEB_EVENTS)


def write_browsing():
    outbound_browsing_log_filename = os.path.join(OUTPUT_PATH, "weblog.txt")
    with open(outbound_browsing_log_filename, 'w+') as f:
        for event in WEB_EVENTS:
            f.write(event)
            f.write("\n")

    


#def gen_web_server_data():
#    """Generate web server logs"""
#    pass





gen_emails()
gen_browsing(10)
inject_malicious_emails()
inject_malicious_traffic()