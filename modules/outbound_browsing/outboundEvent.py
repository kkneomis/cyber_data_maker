import random
import string

from faker import Faker
from faker.providers import internet
from faker.providers import user_agent

# instantiate faker
fake = Faker()
fake.add_provider(internet)

METHODS = ["GET"]
STATUS_CODES = ["202", "301", "302", "404", "403"]


class OutboundEvent:

    def __init__(self, time, src_ip, dst_ip, user_agent, url, request=None):
        """Set initial values"""
        self.time = time
        self.src_ip = src_ip
        self.user_agent = user_agent
        self.dst_ip = dst_ip
        self.set_method()
        self.set_status_code()

        self.url = url or fake.uri()
        parsed_link = url.split("//")[-1].split("/")
        self.host = parsed_link[0].split('?')[0]

        self.request = request or '/'.join(parsed_link[1:])


    def set_method(self):
        """
        Request method
        e.g. GET, POST PUT
        Currently limited to GET ONLY
        """
        self.method = random.choice(METHODS)

    def set_status_code(self):
        """
        Result of the request
        Chosen randomly from status codes defined above
        """
        self.status_code = random.choice(STATUS_CODES)

    def stringify(self):
        """Print the data in one convinient line"""
        logline = ' '.join([str(x) for x in [self.time, self.method, self.src_ip, self.url, 
                                             self.request, self.dst_ip, self.user_agent]])

        return logline 

        '''
        return  { "time": self.time, 
                  "method": self.method, 
                  "src_ip": self.src_ip, 
                  "host": self.host, 
                  "request": self.request, 
                  "dst_ip": self.dst_ip, 
                  "user"self.user_agent]])
        '''

