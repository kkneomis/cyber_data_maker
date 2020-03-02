class InboundEvent:
        
    def __init__(self, time, external_hosts, internal_endo):
        """Set initial values"""
        self.hosts = external_hosts
        self.endpoints = endpoints
        self.time = time
        self.set_new_user()
        self.set_new_endpoint()
        self.src_addr = self.current_user["ip_addr"]
        self.user_agent = self.current_user["user_agent"]
        self.username = self.current_user["username"]
        self.url = self.current_endpoint
        self.set_method()
        self.set_response_code()
    
    def set_new_user(self):
        self.current_user = random.choice(HOSTS)
        
    def set_new_endpoint(self):
        self.current_endpoint = "/" + random.choice(endpoints)
        
    def set_method(self):
        self.method = random.choice(METHODS)
    
    def set_response_code(self):
        self.response_code = random.choices(STATUS_CODES,[.8, .1, .1], k=1)[0]
    
    def get_event(self):
        """Print the data in one convenient line"""
        logline = "%s %s %s %s %s %s" % (self.time, self.username, self.src_addr, self.method, self.url, self.response_code)

        return logline