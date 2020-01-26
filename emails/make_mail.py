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


def gen_email_log(date_time, sender_domains, sender, recipient, corpus):
    """
    Takes in a time, sender, and recipient
    Returns a list for dicts representing an email received
    """        
    # generate this on the fly using datetime functions similar to other scripts
    date_time = date_time + timedelta(seconds=random.randint(200, 3000))
    time = date_time.strftime("%a %b %d %H:%M:%S %Y")

    # get this from the list of active company employess

    body = generate_text(corpus, 20)
    subject = generate_text(corpus, 7)

    # create a hash of the datetime for message naming
    hash = hashlib.sha1()
    hash.update(str(time))
    filename =  "email_%s" % hash.hexdigest()

    result = random.choice(["Accepted", "Blocked"])
   

    # write the email to file
    # with open(filename, 'w') as f:
    #    f.write(content)

    # cache the method in a json object for replies
    cur_message = {
                    "event_time": time,
                    "sender":sender,
                    "recipient":recipient,
                    "filename":filename,
                    "subject":subject,
                    "result": result
                  }
                
    return cur_message


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
                        subject = email['subject'])        

    filename = os.path.join(output_path, email['filename'])
    # write the email to file
    with open(filename, 'w+') as f:
       f.write(content)


