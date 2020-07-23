import os
import random, json
import urllib.parse
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
    INFECTED_HOSTS = []
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
                time = parse(email.time) + timedelta(seconds=random.randint(0, 100))
                if not dst_ip:
                    # this was a made up email domain. it is not mapped to an IP in our file of domains
                    # give it a fake IP on the spot
                    ip = fake.ipv4
                else:
                    # we want to log defined malicious links so these hosts can beacon out later
                    infected_host = {
                        "src_ip":src_ip,
                        "user_agent":user_agent,
                        "time":time
                    }
                    INFECTED_HOSTS.append(infected_host)
                new_event = OutboundEvent(time=time, src_ip=src_ip, dst_ip=dst_ip,  url=url, user_agent=user_agent).stringify()
                WEB_EVENTS.append(new_event)

    return WEB_EVENTS, INFECTED_HOSTS


def beacon_out(host, **config):
    """
    This function emulates a compromised machine beaconing to a c2 domain
    Given a command and control domain, beacon out to it periodically
    """
    mal_config = config["mal_config"]
    src_ip=host["src_ip"]
    dst_ip= random.choice(mal_config["c2"])
    c2_host = "http://" + dst_ip
    #c2_domain =  random.choice(**config["c2"])
    user_agent=host["user_agent"]
    start_time=host["time"]

    # reference http://lpc1.clpccd.cc.ca.us/lpc/mdaoud/CNT7501/NETLABS/Ethical_Hacking_Lab_01.pdf
    # more these to come later - result of additional research
    commands = [
        "net view",
        "net view /domain",
        "net view /domain:Administrators",
    ]
    clock = Clock(start=start_time, interval=4000)
    beacon_events = []

    for command in commands:
        clock.tick()
        # we can't have allll of the data so we need to settle here
        # there will be no responses provide, just web requests
        # so here is what the c2 will look like:
        # c2domain.com/listner.php?c={command} (where the command is encoded somehow)
        # followed by the response to the command
        # let's try a sequence
        # 1. request to c2domain
        #     c2domain.com/listener.php?c={syn, hostname}
        # 2. interpret command 2
        #     c2domain.com/listener.php?c={ack, whoami}
        #     c2domain.com/listener.php?c={hostname: hostname}
        command = '/listener.php?c={"syn": "%s"}' % command
        command = urllib.parse.quote(command)
        new_event = OutboundEvent(time=clock.get_time(), src_ip=src_ip, dst_ip=dst_ip,  url=c2_host, 
                                  request=command, user_agent=user_agent).stringify()
        beacon_events.append(new_event)

    return beacon_events


