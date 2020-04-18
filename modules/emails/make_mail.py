import sys
import os

from datetime import datetime
from dateutil.parser import parse
from datetime import timedelta
import random
import json
import hashlib

date_time = datetime(1988, 6, 29, 8, 00, 00)

class Email:

    def __init__(self, date_time, sender, recipient, subject, body, result=None, link=None, reply_to=None):

        self.time = date_time.strftime("%a %b %d %H:%M:%S %Y")
        self.subject = subject
        self.body = body
        self.sender = sender
        self.recipient = recipient
        self.hash = self.get_hash()

        self.filename = filename = "email_%s" % self.hash.hexdigest()
        self.link = link
        
        if not result:
            self.result = random.choice(["Accepted", "Blocked"])
        else:
            self.result = result

        if not link:
            self.link = gen_link()
        else:
            self.link = link

        if not reply_to:
            self.reply_to = sender
        else:
            self.reply_to = reply_to
            

    def stringify(self):
        """return json object with email attributes"""
        return {
            "event_time": self.time,
            "sender": self.sender,
            "reply_to": self.reply_to,
            "recipient": self.recipient,
            "filename": self.filename,
            "subject": self.subject,
            "body": self.body,
            "result": self.result,
            "link": self.link
        }
    
    def stringifysimple(self):
        """return json object with email attributes"""
        return {
            "event_time": self.time,
            "sender": self.sender,
            "reply_to": self.reply_to,
            "recipient": self.recipient,
            "filename": self.filename,
            "subject": self.subject,
            "result": self.result
        }

    def get_hash(self):
        val = str(self.time) + self.sender
        hash = hashlib.sha1(str(val).encode('utf-8'))
        return hash


def gen_link():
    """Generate random strings of three words for dummy url"""
    # thanks to: https://www.geeksforgeeks.org/python-remove-all-characters-except-letters-and-numbers/
    import re
    pre = random.choice(["http://",
                         "https://",
                         "www.",
                         "http://wwww.",
                         "https://www.", ""])
    tld = random.choice([".com", ".org", ".net", ".biz", ".co", ".co.uk"])
    ini_string = generate_text("time person year way day thing man world life hand part child eye woman place work week case point government company number group problem fact good new first last long great little own other old right big high different small large next early young important few public bad same able", 3)
    # remove non-alphanumeracal characters
    domain = re.sub('[\W_]+', '', ini_string).lower()
    link = pre + domain + tld
    return link

def generate_text(corpus, length):
    words = [x.strip() for x in corpus.split(' ')]
    final_text = ""
    word = random.choice(words)
    for i in range(length):
        final_text = final_text + word + " "
        word = random.choice(words)
    return final_text


