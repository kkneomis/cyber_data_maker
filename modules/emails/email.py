import sys
import os

from datetime import datetime
from dateutil.parser import parse
from datetime import timedelta
import random
import json
import hashlib

from faker import Faker
from faker.providers import internet

# instantiate faker
fake = Faker()
fake.add_provider(internet)

class Email:

    def __init__(self, date_time, sender, recipient, subject, body, result=None, link=None, reply_to=None):

        self.time = date_time.strftime("%a %b %d %H:%M:%S %Y")
        self.subject = subject
        self.body = body
        self.sender = sender
        self.recipient = recipient
        self.hash = self.get_hash()

        
        self.link = link
        
        if not result:
            self.result = random.choice(["Accepted", "Blocked"])
        else:
            self.result = result

        if self.result == "Accepted":
            self.filename = "email_%s" % self.hash.hexdigest()
        else:
            self.filename = "N/A"

        if not link:
            self.link = fake.uri()
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



