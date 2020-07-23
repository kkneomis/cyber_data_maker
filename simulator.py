import os
import json
import random
import base64
import ipaddress
import shutil

from faker import Faker
from faker.providers import internet
from faker.providers import person
from faker.providers import user_agent
from faker.providers import file

# instantiate faker
fake = Faker()
fake.add_provider(internet)
fake.add_provider(person)
fake.add_provider(user_agent)
fake.add_provider(file)


WORD_CLOUD = ["account", "site", "user", "microsoft", "twitter", "it", "reset", "download", "org", "digital",
              "invoice", "payment", "secure", "notice", "critical", "financial", "bank", "service",
              "business", "portal", "browse", "legit", "defender", "login", "share", "amazon", "device"]

EMAIL_DOMAINS = ["@gmail.com", "@yahoo.com", "@hotmail.com", "@protonmail.com"]

def get_subject(num_subjects):
    """
    Return a list with the specfied number of subjects from our master list
    """
    with open("config/general/simulation/malicious_subjects.txt") as f:
        data = f.readlines()

    # get n random subjects
    subjects = random.sample(data, num_subjects)
    # remove trailing newlines
    subjects = [s.rstrip() for s in subjects]

    return subjects


def gen_sender_addr():
    """
    Generate a malicious sender email address
    """
    prefix = "".join(random.sample(WORD_CLOUD, 2))
    domain = random.choice(EMAIL_DOMAINS)
    sender_addr = prefix + domain

    return sender_addr


def gen_senders(senders_count=5):
    return [gen_sender_addr() for n in range(senders_count)]


def gen_link():
    """Generate random strings of three words for dummy url"""
    # thanks to: https://www.geeksforgeeks.org/python-remove-all-characters-except-letters-and-numbers/
    import re
    pre = random.choice(["http://",
                         "https://",
                         "http://www.",
                         "https://www."])
    tld = random.choice([".com", ".org", ".net", ".co", ".info", ".co.uk"])
    domain = "".join(random.sample(WORD_CLOUD, 3))

    request = fake.file_name(category="office", extension="exe")
    
    #"".join(random.sample(WORD_CLOUD, 3))
    #encodedBytes = base64.b64encode(request.encode("utf-8"))
    #request = encodedBytes.decode('utf-8')

    link = pre + domain + tld + "/" + request
    return link


def gen_links():
    """Generate a random number of links/IP pairs"""
    num = random.randint(2, 7)
    links = []
    for _ in range(num):
        links.append({
                "url": gen_link(),
                "ip": fake.ipv4_public()
            })

    return links


def get_user_agent():
    """
    get a random user agent from a list
    """
    with open("config/general/user_agents.txt") as f:
        agent = f.readlines()
    return random.choice(agent).strip()


def gen_email_addr(name):
    """
    take a name and made and make an email addr
    """
    pass


def gen_users(count_employees=10):
    with open("config/general/simulation/companies.json") as f:
        data = json.loads(f.read())

    ip = ipaddress.ip_address(fake.ipv4_private())
    company = random.choice(data)
    domain = "".join(company["company_name"].split(" ")).lower() + ".com"
    employees = [fake.name() for n in range(count_employees)]
    users = []

    for employee in employees:
        user = {}
        user["name"] = employee
        user["email_addr"] = ".".join(
            employee.split(" ")).lower() + "@" + domain
        user["user_agent"] = fake.user_agent()
        user["ip_addr"] = str(ip)
        ip += 1
        users.append(user)

    company["employees"] = users

    return company

def set_up_output_dir(OUTPUT_PATH):
    """
    Remove output folder if exists
    Create a new one
    """
    #try:
    shutil.rmtree(OUTPUT_PATH, ignore_errors=False, onerror=None)
    #except:
    #    print('Error while deleting directory')
    os.mkdir(OUTPUT_PATH)
 
def run_simulation(level):
    malicious_config = {}
    company_info = {}

    subject_count = int(level/2)

    set_up_output_dir('config/changeme/simulated')

    malicious_config["blocked_subjects"] = get_subject(subject_count)
    malicious_config["accepted_subjects"] = get_subject(subject_count)
    malicious_config["senders"] = gen_senders(min(level, 20))
    malicious_config["reply_to"] = [gen_sender_addr()]
    malicious_config["links"] = gen_links()
    malicious_config["c2"] = [fake.ipv4_public()]

    company_info = gen_users(count_employees=max(level, 5))

    with open('config/changeme/simulated/company.json', 'w+') as f:
        f.write(json.dumps(company_info, indent=4))

    with open('config/changeme/simulated/malicious.json', 'w+') as f:
        f.write(json.dumps(malicious_config, indent=4))

    return 'config/changeme/simulated'


if __name__== "__main__":
    run_simulation()
    print("New config at config/changeme/simulated/company.json")
    print("New config at config/changeme/simulated/malicious.json")
