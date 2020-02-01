import random 

METHODS = ["GET"]
STATUS_CODES = ["202", "301", "302", "404", "403"]

class OutboundEvent:
        
    def __init__(self, time, hosts, endpoints):
        """Set initial values"""
        self.time = time
        self.hosts = hosts
        self.endpoints = endpoints
        self.set_new_user()
        self.set_new_endpoint()
        self.src_addr = self.current_user["ip_addr"]
        self.user_agent = self.current_user["user_agent"]
        self.url = self.current_endpoint
        self.set_method()
        self.set_status_code()
        
    
    def set_new_user(self):
        self.current_user = random.choice(self.hosts)
        
    def set_new_endpoint(self):
        self.current_endpoint = random.choice(self.endpoints)
        
    def set_method(self):
        self.method = random.choice(METHODS)
    
    def set_status_code(self):
        self.status_code = random.choice(STATUS_CODES)
    
    def get_event(self):
        """Print the data in one convinient line"""
        logline = "%s %s %s %s %s" % (self.time, self.method, self.src_addr, self.url, self.user_agent)

        return logline
