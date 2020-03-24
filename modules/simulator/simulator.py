import json
import random
import base64

malicious_config = {}
employee_config = {}
challenge_meta = {}

WORD_CLOUD = [ "account", "site", "user", "microsoft", "twitter", "it", "reset", "download", "org", "digital",
                "invoice", "payment", "secure", "notice", "critical", "financial", "bank", "service",
                "business", "portal", "browse", "legit", "defender", "login", "share", "amazon", "device"]

EMAIL_DOMAINS = ["@gmail.com", "@yahoo.com", "@hotmail.com", "@protonmail.com"]


def get_subject(num_subjects):
    """
    Return a list with the specfied number of subjects from our master list
    """
    with open("../../config/general/simulation/malicious_subjects.txt") as f:
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

def gen_sender():
    num = random.randint(1, 5)
    senders = []
    for _ in range(num):
        senders.append(
            gen_sender_addr()
        )


def gen_link():
    """Generate random strings of three words for dummy url"""
    # thanks to: https://www.geeksforgeeks.org/python-remove-all-characters-except-letters-and-numbers/
    import re
    pre = random.choice(["http://",
                        "https://",
                        "www.", 
                        "http://wwww.",
                        "https://www.", ""])
    tld = random.choice([".com", ".org", ".net", ".co", ".info", ".co.uk"])
    domain = "".join(random.sample(WORD_CLOUD, 3))

    request = "".join(random.sample(WORD_CLOUD, 3))
    encodedBytes = base64.b64encode(request.encode("utf-8"))
    request = str(encodedBytes, "utf-8")

    link = pre + domain + tld + "/" + request
    return link

def gen_ip():
    """Create a dummy IP addr"""
    return ".".join(map(str, (random.randint(0, 255)  for _ in range(4))))


def gen_links():
    """Generate a random number of links/IP pairs"""
    num = random.randint(2,7)
    links = []
    for _ in range(num):
        links.append(
            {
                "url":gen_link(),
                "ip":gen_ip()
            }
        )
    
    return links

    

malicious_config["blocked_subjects"] = get_subject(5)
malicious_config["accepted_subjects"] = get_subject(2)
malicious_config["senders"] = gen_sender_addr()
malicious_config["reply_to"] = [gen_sender_addr()]
malicious_config["links"] = gen_links()

print(gen_links())
print(json.dumps(malicious_config, indent=4))