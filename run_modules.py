import os
import shutil
import random
import copy
import json

from jinja2 import Template
from datetime import datetime
from dateutil.parser import parse
from datetime import timedelta
from tqdm import tqdm

from modules.emails.make_mail import Email
from modules.emails.make_mail import create_email_obj
from modules.outbound_browsing.make_outbound_traffic import OutboundEvent
from modules.clock.clock import Clock

employees = "config/employees.json"

date_time = datetime(2020, 6, 29, 8, 00, 00)


with open('config/changeme/challenge_meta.json') as f:
    challenge_info = json.loads(f.read())

# load up the company's employees
with open('config/changeme/employees.json') as f:
    hosts = json.loads(f.read())

# config for the adversary data
with open('config/changeme/malicious.json', 'r') as f: 
    mal_config = json.loads(f.read())

# body of text used to generate emails and other goodies
with open('config/changeme/corpus.txt') as f:
    corpus  = f.read()
    
# load up the fake email sender names
with open('config/general/names.txt') as f:
    sender_names = f.readlines()

# domains for fake email sender
with open('config/general/domains.txt') as f:
    sender_domains = f.readlines()

# email templates to be populated
with open('config/general/templates/email_jinja_template.txt') as f:
    template_text = f.read()

# dummy websites that users visit
with open('config/general/external_hosts.txt', 'r') as f: 
    endpoints = f.readlines()



#template_obj = Template(template_text)
TEMPLATE_OBJ = Template(template_text)
MAIL_LOG = []
WEB_EVENTS = []
MALICIOUS_EMAIL_COUNT = 10

def gen_email_addr():    
    name = random.choice(sender_names).lower().strip().replace(" ", ".")
    domain = random.choice(sender_domains).strip()
    return "%s@%s"% (name, domain)

OUTPUT_PATH = "output/"
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

def gen_emails(num=3):
    """
    Generate a log of background email activity 
    Emails are either accepted or blocked
    Generate email files for accepted emails the logs
    """
    clock = Clock(start=date_time, interval=3000)
    
    # creating {num} number of emails and adding the mail log
    print("Generating email objects...")
    for i in tqdm(range(num)):
        time = clock.get_time()
        # generate a random float to represent probably of malicious email
        # 20% of the time, make the email malicious targeted
        # until we've generated the necessary number of malicious emails
        malicious = random.random()
        global MALICIOUS_EMAIL_COUNT
        if malicious <= .2 and MALICIOUS_EMAIL_COUNT > 0:
            # generate a targeted malicious email
            inject_malicious_emails(time)
            MALICIOUS_EMAIL_COUNT -= 1
        else:
            # otherwise generate noise email
            sender = gen_email_addr()
            recipient = random.choice(hosts)["email_addr"]
            
            result = Email(time, sender_domains, sender, recipient, corpus).stringify()
            
            MAIL_LOG.append(result)
            clock.tick()
        

    


def inject_malicious_emails(time):
    """Generate emails from malicious senders"""

    # creating {num} number of emails and adding the mail log
    sender = random.choice(mal_config["senders"])
    result = random.choice(["Accepted", "Blocked"])
    reply_to = random.choice(mal_config["reply_to"])

    if result == "Accepted":
        # generate accepted emails
        recipient = random.choice(hosts)["email_addr"]
        subject = random.choice(mal_config["accepted_subjects"])
        link = random.choice(mal_config["links"])["url"]
        new_mail = Email(time, sender_domains, sender, recipient, corpus, 
                        result="Accepted", subject=subject, link=link, reply_to=reply_to)
        MAIL_LOG.append(new_mail.stringify())
    else:
        # generate blocked emails
        recipient = random.choice(hosts)["email_addr"]
        subject = random.choice(mal_config["blocked_subjects"])
        link = random.choice(mal_config["links"])["url"]
        new_mail = Email(time, sender_domains, sender, recipient, corpus,
                             result="Blocked", subject=subject, link=link, reply_to=reply_to)
        MAIL_LOG.append(new_mail.stringify())


def gen_browsing(num):
    """Generate fake web browsing traffic"""
    clock = Clock(start=date_time, interval=400)
    
    print("Generating %s web browsing evants..." % num)
    for i in tqdm(range(num)):
        time = clock.get_time()
        new_event = OutboundEvent(time, hosts, endpoints).stringify()
        WEB_EVENTS.append(new_event)

        clock.tick()


def inject_malicious_traffic():
    """General traffic of users clicking bad links
    Make this trigger after malicious email is injected
    """

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
        if "google.com" not in event["link"]:
            #and event["result"] == "Accepted"
            user = get_user_from_email(event["recipient"])
            link = event["link"]
            parsed_link = link.split("//")[-1].split("/")
            domain = parsed_link[0].split('?')[0]
            request = '/'.join(parsed_link[1:])
            ip = get_link_ip(link)
            if not ip:
                # this was a made up email domain. it is not mapped to an IP in our file of domains
                # give it a fake IP on the spot
                ip = ".".join(map(str, (random.randint(0, 255)  for _ in range(4))))
            time = parse(event["event_time"]) + timedelta(seconds=random.randint(0, 100))
            endpoint = "%s/ %s" % (domain, ip)
            new_event = OutboundEvent(time, hosts, endpoints, 
                                     user=user, endpoint=endpoint, request=request).stringify()
            WEB_EVENTS.append(new_event)


def write_browsing():
    """Write web browsing events to file"""
    outbound_browsing_log_filename = os.path.join(OUTPUT_PATH, "weblog.txt")
    with open(outbound_browsing_log_filename, 'w+') as f:
        for event in WEB_EVENTS:
            f.write(event)
            f.write("\n")


def write_email():
    """ 
    write json email objects to file 
    write full email bodies to files
    """
    # output dictories for the logs and email fiels
    email_log_filename = os.path.join(OUTPUT_PATH, "mail_logs.json")
    email_file_dir = os.path.join(OUTPUT_PATH, "emails")

    # create the email output directory if it doesn't already exist
    if not os.path.exists(email_file_dir):
        os.makedirs(email_file_dir)

    with open(email_log_filename, 'a') as f:
        for email in MAIL_LOG:
            # we don't want to print the link in the json email log
            # but we need it for other things
            # so make a close instead and delete the link key from the dict
            email_tmp = copy.deepcopy(email)
            del email_tmp['link']
            f.write(json.dumps(email_tmp))
            f.write("\n")

    # generate email files
    print("Generating email files...")
    for email in tqdm(MAIL_LOG):
        # we are only generating files for accepted emails
        if email['result'] != "Blocked":
            content = create_email_obj(email, corpus, TEMPLATE_OBJ, email_file_dir)
            email_filename = os.path.join(email_file_dir, email['filename'])
            with open(email_filename, 'w+') as f:
                f.write(content)



#def gen_web_server_data():
#    """Generate web server logs"""
#    pass


def set_up_output_dir():
    """
    Remove output folder if exists
    Create a new one
    """
    shutil.rmtree('output')
    print('Removed existing output dir...')
    os.mkdir('output')
    print('Created a new output dir...')

def add_employee_data():
    """Add employee info to the output"""
    print("Adding employee info to output....")
    with open('output/employees.json', 'w+') as f:
        f.write(json.dumps(hosts, indent=4))


def make_questions():
    """Generate question set""" 
    print("Generating questions....")
    with open('config/questions/base.txt') as f:
        text = f.read()
        template = Template(text)

    title = challenge_info["title"]
    company = challenge_info["company_name"]
    description = challenge_info["description"]
    malicious_sender = random.choice(mal_config["senders"])

    content =  template.render(title = title,
                               company = company,
                               description = description,
                               malicious_sender = malicious_sender)

    with open('output/prompt.txt', 'w+') as f:
        f.write(content)



set_up_output_dir()
gen_emails(100)
gen_browsing(1000)
inject_malicious_traffic()
write_browsing()
write_email()
make_questions()
add_employee_data()