import os
import random, json
from datetime import datetime
from dateutil.parser import parse
from datetime import timedelta

from tqdm import tqdm

from faker import Faker
from faker.providers import internet
from faker.providers import user_agent

from modules.outbound_browsing.outboundEvent import OutboundEvent
from modules.clock.clock import Clock 

#============================================
# Set up all the configs
#============================================

# instantiate faker
fake = Faker()
fake.add_provider(internet)
fake.add_provider(user_agent)

#============================================
# Generate the outbound browsing data
#============================================

def gen_browsing(count=100, **config):
    """Generate fake web browsing traffic"""
    WEB_EVENTS = []
    hosts = config["hosts"]


    date_time = datetime(2020, 6, 29, 8, 00, 00)
    clock = Clock(start=date_time, interval=400)

    print("Generating %s web browsing events..." % count)
    for i in tqdm(range(count)):
        time = clock.get_time()

        host = random.choice(hosts)
        src_ip = host["ip_addr"]
        user_agent = host["user_agent"]
        dst_ip = fake.ipv4()
        url = fake.uri()
        
        new_event = OutboundEvent(time, src_ip, dst_ip, user_agent, url).stringify()
        WEB_EVENTS.append(new_event)

        clock.tick()

    return WEB_EVENTS


def click_links(MAIL_LOGS, CLICK_RATE=.7, **config):
    """
    Given a list of json mail events, click the links in object
    """
    WEB_EVENTS = []
    hosts = config["hosts"]
    mal_config = config["mal_config"]

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

    for email in MAIL_LOGS:
        click = random.random()
        # There is a 70% chance of users clicking each link
        if click < CLICK_RATE:
            if email.link and email.result == "Accepted":
                user = get_user_from_email(email.recipient)
                src_ip = user["ip_addr"]
                user_agent = user["user_agent"]
                url = email.link
                dst_ip = get_link_ip(url)
                if not dst_ip:
                    # this was a made up email domain. it is not mapped to an IP in our file of domains
                    # give it a fake IP on the spot
                    ip = fake.ipv4
                time = parse(email.time) + timedelta(seconds=random.randint(0, 100))
                new_event = OutboundEvent(time=time, src_ip=src_ip, dst_ip=dst_ip,  url=url, user_agent=user_agent).stringify()
                WEB_EVENTS.append(new_event)

    return WEB_EVENTS

