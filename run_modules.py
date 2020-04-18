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
from modules.outbound_browsing.make_outbound_traffic import OutboundEvent
from modules.clock.clock import Clock

import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument(
    '--config_path', type=str, default="config/changeme/default/",
                    help='Path to config containing employee and malicous config. Defaults to config/changeme/default')

args = parser.parse_args()

date_time = datetime(2020, 6, 29, 8, 00, 00)

config_path = args.config_path

# load up the company's employees
company_info_config = os.path.join(config_path, "company.json")
with open(company_info_config, 'r') as f:
    company_info = json.loads(f.read())

hosts = company_info["employees"]

# config for the adversary data
malicious_config = os.path.join(config_path, "malicious.json")
with open(malicious_config, 'r') as f:
    mal_config = json.loads(f.read())

# body of text used to generate emails and other goodies
corpus_config = os.path.join(config_path, "corpus.txt")
try:
    with open(corpus_config, 'r') as f:
        corpus = f.read()
except FileNotFoundError:
    print("Hmmm... there appears ot be no corpus at this location. Using the default.")
    with open("config/changeme/default/corpus.txt", 'r') as f:
        corpus = f.read()

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

# template_obj = Template(template_text)
TEMPLATE_OBJ = Template(template_text)
MAIL_LOG = []
WEB_EVENTS = []
MALICIOUS_EMAIL_COUNT = 10


def gen_email_addr():
    name = random.choice(sender_names).lower().strip().replace(" ", ".")
    domain = random.choice(sender_domains).strip()
    return "%s@%s" % (name, domain)


OUTPUT_PATH = "output/"
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)


config_path = "config/changeme/default/" #args.config_path


email_body_config = os.path.join(config_path, "email_body.json")
try:
    with open(email_body_config, 'r') as f:
        email_body = json.loads(f.read())
except Exception as e:
    print("Hmmm... there appears to be no json at this location. Using the default.")
    with open("config/general/email_body.json", 'r') as f:
        email_body = json.loads(f.read())    

        
def gen_emails(num=10, malicious_emails=10):
    clock = Clock(start=date_time, interval=3000)
    email_log_filename = os.path.join(OUTPUT_PATH, "mail_logs.json")
    email_file_dir = os.path.join(OUTPUT_PATH, "emails")
    
    # creating {num} number of emails and adding the mail log
    print("Generating email objects...")
    for i in tqdm(range(num)):
        emailtype = ""
        is_malicious = False
        is_internal = False
        time = clock.get_time()
        mailtype = random.random()
        if mailtype <= .2 and malicious_emails > 0:   # Is malicious
            # generate a targeted malicious email
            is_malicious = True
            malicious_emails -= 1
            emailtype = "malware"
        elif mailtype <= .8:  #Is Internal
            is_internal = True
            emailtype = "internal"
        else: #Is External
            is_internal = False
            emailtype = "external"
        
        email = do_email(time, emailtype)
        # Save Email to file
        if email.result != "Blocked":
            t = TEMPLATE_OBJ

            content = t.render(body=email.body,
                       sender=email.sender,
                       reply_to=email.reply_to,
                       time=email.time,
                       recipient=email.recipient,
                       subject=email.subject,
                       link=email.link if emailtype == "malware" else random.choice(["", "", email.link]))
            email_filename = os.path.join(email_file_dir, email.filename)
            with open(email_filename, 'w+') as f:
                f.write(content)
        # Log Email 
        MAIL_LOG.append(email)
        with open(email_log_filename, 'a') as f:
            f.write(json.dumps(email.stringifysimple()))
            f.write("\n")
        clock.tick()
        
        
def do_email(date_time, emailtype):
    datum = email_body[emailtype]
    data = random.choice( datum )
    sender = ""
    recipient = random.choice(hosts)["email_addr"]
    while ((sender == "") or (sender==recipient)):
        if emailtype == "internal":
            sender = random.choice(hosts)["email_addr"]
            result = "Accepted"
            link = None
        elif emailtype == "external":
            sender = gen_email_addr()
            result = "Accepted"
            link = None
        else:
            sender = random.choice(mal_config["senders"])
            result = random.choice(["Accepted", "Blocked"])
            link = random.choice(mal_config["links"])["url"]
    #     subject = random_string(data['subject'])
    #     body = random_string(data['body'])
    subject, body = random_string2(data['subject'],data['body'])
    # ADD HANDLING FOR MALICIOUS EMAILS

    result = Email(date_time, sender, recipient, subject, body, result, link=link)
    return result
        
        
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
        if "google.com" not in event.link:
            # and event["result"] == "Accepted"
            user = get_user_from_email(event.recipient)
            link = event.link
            parsed_link = link.split("//")[-1].split("/")
            domain = parsed_link[0].split('?')[0]
            request = '/'.join(parsed_link[1:])
            ip = get_link_ip(link)
            if not ip:
                # this was a made up email domain. it is not mapped to an IP in our file of domains
                # give it a fake IP on the spot
                ip = ".".join(
                    map(str, (random.randint(0, 255) for _ in range(4))))
            time = parse(event.time) + timedelta(
                seconds=random.randint(0, 100))
            endpoint = "%s/ %s" % (domain, ip)
            new_event = OutboundEvent(time, hosts, endpoints,
                                      user=user, endpoint=endpoint, request=request).stringify()
            WEB_EVENTS.append(new_event)        
        
        
def random_string(corpus):
    while True:
        container = find_next_container(corpus)
        if container == "":
            break
        else:
            token = choose_token(container)
            corpus = corpus.replace(container, token, 1)
    return corpus

def random_string2(sub, bod):
    while True:
        container = find_next_container(sub)
        if container == "":
            break
        else:
            token = choose_token(container)
            sub = sub.replace(container, token)
            bod = bod.replace(container, token)
    while True:
        container = find_next_container(bod)
        if container == "":
            break
        else:
            token = choose_token(container)
            bod = bod.replace(container, token)
    return sub, bod

def find_next_container(blurb):
    s = blurb.find('<<')
    e = blurb.find('>>')
    if s > -1:
        return (blurb[s:e+2])
    else:
        return ("")
    
def choose_token(container):
    container = container[2: -2]
    terms = container.split('||')
    term = random.choice(terms)
    return term


def gen_browsing(num):
    """Generate fake web browsing traffic"""
    clock = Clock(start=date_time, interval=400)

    print("Generating %s web browsing evants..." % num)
    for i in tqdm(range(num)):
        time = clock.get_time()
        new_event = OutboundEvent(time, hosts, endpoints).stringify()
        WEB_EVENTS.append(new_event)

        clock.tick()



def write_browsing():
    """Write web browsing events to file"""
    outbound_browsing_log_filename = os.path.join(OUTPUT_PATH, "weblog.txt")
    with open(outbound_browsing_log_filename, 'w+') as f:
        for event in WEB_EVENTS:
            f.write(event)
            f.write("\n")


# def gen_web_server_data():
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
    os.mkdir('output/emails')
    print('Created a new emails dir...')


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

    company = company_info["company_name"]
    description = company_info["description"]
    malicious_sender = random.choice(mal_config["senders"])

    content = template.render(company=company,
                              description=description,
                              malicious_sender=malicious_sender)

    with open('output/prompt.txt', 'w+') as f:
        f.write(content)


set_up_output_dir()
gen_emails(100)
gen_browsing(1000)
inject_malicious_traffic()
write_browsing()
make_questions()
add_employee_data()
