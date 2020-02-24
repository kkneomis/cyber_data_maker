import sys
import os

from datetime import datetime
from datetime import timedelta
import random
import nltk
import json 
import hashlib
from utils import *

    
date_time = datetime(1988, 6, 29, 8, 00, 00)

class Email:

    def __init__(self, date_time, sender_domains, sender, 
                recipient, corpus, result=None, subject=None, link=None):

        self.time = date_time.strftime("%a %b %d %H:%M:%S %Y")
        self.body = generate_text(corpus, 20)
        
        self.hash = self.get_hash()
        self.sender = sender
        self.recipient = recipient
        self.filename = filename =  "email_%s" % self.hash.hexdigest() 
        self.link = link
        if not result:
            self.result = random.choice(["Accepted", "Blocked"])
        else:
            self.result = result

        if not subject:
            self.subject = generate_text(corpus, 7)
        else:
            self.subject = subject

        if not link:
            self.link = gen_link(corpus)
        else:
            self.link = link
        
    def stringify(self):
        """return json object with email attributes"""
        return {
                    "event_time": self.time,
                    "sender": self.sender,
                    "recipient": self.recipient,
                    "filename": self.filename,
                    "subject": self.subject,
                    "result": self.result,
                    "link":self.link
                  }

    def get_hash(self):
        hash = hashlib.sha1()
        hash.update(str(self.time))
        return hash

    
def generate_text(corpus, length):
    """
    Use nlkt to generate a paragraph of a given length
    given some feeder text
    """

    words = [x.strip() for x in corpus.split(' ')] 
    # NLTK shortcuts :)
    bigrams = [b for b in zip(words[:-1], words[1:])]
    cfd = nltk.ConditionalFreqDist(bigrams)

    # pick a random word from the corpus to start with
    word = random.choice(words)
    # generate 15 more words
    
    final_text = ""
    for i in range(length):
        final_text = final_text + word + " "
        if word in cfd:
            word = random.choice(cfd[word].keys())
        else:
            break

    return final_text


def gen_link(corpus):
    """Generate random strings of three words for dummy url"""
    # thanks to: https://www.geeksforgeeks.org/python-remove-all-characters-except-letters-and-numbers/
    import re
    pre = random.choice(["http://",
                        "https://",
                        "www.", 
                        "http://wwww.",
                        "https://www.", ""])
    tld = random.choice([".com", ".org", ".net", ".biz", ".co", ".co.uk"])
    ini_string = generate_text(corpus, 3)
    domain = re.sub('[\W_]+', '', ini_string).lower()
    link = pre + domain + tld
    return link
    

def create_email_obj(email, corpus, template_obj, output_path):
    """
    Given a list of json objects
    create email files with messages in the output folder
    Corpus is the body of text used to generate the emails
    """
    t = template_obj
    content =  t.render(body = generate_text(corpus, 100),
                        sender = email['sender'],
                        time = email['event_time'],
                        recipient = email['recipient'],
                        subject = email['subject'],
                        link= email['link'])        

    filename = os.path.join(output_path, email['filename'])
    # write the email to file
    with open(filename, 'w+') as f:
       f.write(content)


