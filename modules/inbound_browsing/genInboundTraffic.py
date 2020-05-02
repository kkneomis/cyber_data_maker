import random
import os
from datetime import datetime
from tqdm import tqdm

from faker import Faker
from faker.providers import internet
from faker.providers import user_agent

from modules.inbound_browsing.inbound_event import InboundEvent
from modules.clock.clock import Clock 

#============================================
# Set up all the configs
#============================================

# instantiate faker
fake = Faker()
fake.add_provider(internet)
fake.add_provider(user_agent)


with open("config/general/malicious_request.txt") as f:
    malicious_requests = f.readlines()

with open("config/general/benign_request.txt") as f:
    benign_request = f.readlines()

inbound_browsing_log_filename = "output/inbound_proxy_traffic.txt"

#============================================
# Create the outbound traffic
#============================================

def gen_inbound_traffic(count=1000, **config):
    """
    Create a list of inbound events
    """
    events = []
    server_domain = config["company_domain"]
    clock = Clock(start=config["start_time"], interval=400)

    for _ in tqdm(range(count)):
        ip = fake.ipv4()
        ua = '\"%s\"' % fake.user_agent()

        type = random.choices(["benign", "malicious"], [.7, .3], k=1)[0]

        for _ in range(random.randint(2,5)):
            if type == "benign":
                request = random.choice(benign_request).rstrip()
                ## auto pass the benign request
                response = random.choice([200, 302])
            else:
                request = random.choice(malicious_requests).rstrip()
                ## auto fail the malicious request
                response = random.choice([500, 404])

            req = InboundEvent(time=clock.get_time(), src_ip=ip, host=server_domain, 
                            user_agent=ua, request=request, method="GET", response_code=response)

            events.append(req.get_event())
            clock.tick()

    # write the generate events to file
    with open(inbound_browsing_log_filename, 'w+') as f:
        for event in events:
            f.write(event)
            f.write("\n")



