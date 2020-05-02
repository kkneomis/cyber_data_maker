import os
import random
import json 

from datetime import datetime
from tqdm import tqdm
from jinja2 import Template

from faker import Faker
from faker.providers import internet

from modules.emails.email import Email
from modules.clock.clock import Clock 

#============================================
# Set up all the configs
#============================================

# instantiate faker
fake = Faker()
fake.add_provider(internet)

config_path = "config/changeme/default/"

# email jinja templates to be populated
with open('config/general/templates/email_jinja_template.txt') as f:
    template_text = f.read()

TEMPLATE_OBJ = Template(template_text)

# get config for generating email bodies
email_body_config = os.path.join(config_path, "email_body.json")
try:
    with open(email_body_config, 'r') as f:
        email_body = json.loads(f.read())
except Exception as e:
    print("Hmmm... there appears to be no json at this location. Using the default.")
    with open("config/general/email_body.json", 'r') as f:
        email_body = json.loads(f.read())    

#============================================
# Make the emails
#============================================

def gen_emails(count=100, malicious_emails=10, **config):
    """
    Generate a list of email objects
    """
    MAIL_LOG = []
    start_time = config["start_time"]
    output_path = config["output_path"]
    mal_config = config["mal_config"]
    hosts = config["hosts"]

    clock = Clock(start=start_time, interval=3000)
    email_log_filename = os.path.join(output_path, "mail_logs.json")
    email_file_dir = os.path.join(output_path, "emails")
    
    # creating {num} number of emails and adding the mail log
    print("Generating %s email objects..." % count)
    for i in tqdm(range(count)):
        emailtype = ""
        is_malicious = False
        is_internal = False
        time = clock.get_time()

        mailtype = random.random()
        if mailtype <= .2 and malicious_emails > 0:   # Is malicious
            # generate an external malicious email
            # this will happen 20% of the time until we have generate
            # the specified number of malicious emails we need
            is_malicious = True
            malicious_emails -= 1
            emailtype = "malware"
        elif mailtype <= .8:  #Is Internal
            # generate an internal email
            # this will occur 60% of the time
            is_internal = True
            emailtype = "internal"
        else: #Is External
            # generate an external email
            # this will occur the remaining 20% of the time
            is_internal = False
            emailtype = "external"
        
        # take the configs generated above and
        # create the email object
        email = do_email(time, emailtype, hosts, mal_config)

        # Save accepted Emails to file
        # using the jinja templating engine
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

            # write the email to file
            with open(email_filename, 'w+') as f:
                f.write(content)

        # Log Email 
        MAIL_LOG.append(email)
        with open(email_log_filename, 'a') as f:
            f.write(json.dumps(email.stringifysimple()))
            f.write("\n")

        clock.tick()

    # return the objects anyway for post-processing (clicking links)
    return MAIL_LOG
        
        
def do_email(date_time, emailtype, hosts, mal_config):
    """
    Generate an email object given a time and email type
    Email type can be internal, exaternal, or malicious
    """
    datum = email_body[emailtype]
    data = random.choice( datum )
    sender = ""
    recipient = random.choice(hosts)["email_addr"]
    while ((sender == "") or (sender==recipient)):
        if emailtype == "internal":
            # create an internal email
            sender = random.choice(hosts)["email_addr"]
            result = "Accepted"
            link = None
        elif emailtype == "external":
            # create a benign external email
            sender = fake.ascii_email()
            result = random.choices(["Accepted", "Blocked"], [.7, .3], k=1)[0]
            link = None
        else:
            # create a malicious email
            sender = random.choice(mal_config["senders"])
            result = random.choices(["Accepted", "Blocked"], [.6, .4], k=1)[0]
            # overide the gerical links created in the email class
            # using one of the links in the malicious config
            link = random.choice(mal_config["links"])["url"]
    #     subject = random_string(data['subject'])
    #     body = random_string(data['body'])
    subject, body = random_string2(data['subject'],data['body'])
    # ADD HANDLING FOR MALICIOUS EMAILS

    result = Email(date_time, sender, recipient, subject, body, result, link=link)
    return result


#============================================
# Helper functions to make the email body
#============================================

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