import random 

class InboundEvent:
    """
    An inbound event represents a request to a company controlled web server
    by an external party (someone browsing your website)
    """

    METHODS = ['GET', 'POST']
    STATUS_CODES = [200, 302, 404, 500]

    def __init__(self, time, src_ip, host, user_agent,  request="/", response_code=None, type="benign", method=None):
        """
        type: benign or malicious
        response: 200 or 302 if benign
                  404 or 500 if malicious
        """

        self.time = time
        self.src_ip = src_ip
        self.host = host
        self.user_agent = user_agent
        self.request = request
        self.response_code = response_code or self.get_response_code()
        self.method = method or self.get_method()

    def get_method(self):
        return random.choices(self.METHODS, [.8, .2], k=1)[0]

    def get_response_code(self):
        return random.choices(self.STATUS_CODES, [.7, .1, .1, .1], k=1)[0]

    def get_event(self):
        """Print the data in one convenient line"""
        logline = ' '.join([str(x) for x in [ self.time, self.src_ip, self.method, self.host, 
                                              self.request, self.user_agent, self.response_code ]])

        return logline
