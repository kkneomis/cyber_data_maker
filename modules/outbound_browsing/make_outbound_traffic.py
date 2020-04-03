import random
import string

METHODS = ["GET"]
STATUS_CODES = ["202", "301", "302", "404", "403"]


class OutboundEvent:

    def __init__(self, time, hosts, endpoints, user=None, endpoint=None, request=None):
        """Set initial values"""
        self.time = time
        self.hosts = hosts
        self.endpoints = endpoints
        if user:
            self.current_user = user
        else:
            self.set_new_user()

        if endpoint:
            self.current_endpoint = endpoint
        else:
            self.set_new_endpoint()

        if request:
            self.request = request
        else:
            self.set_request()

        self.src_ip = self.current_user["ip_addr"]
        self.user_agent = self.current_user["user_agent"]
        self.url = self.current_endpoint.split("/")[0]
        self.dst_ip = self.current_endpoint.split("/")[1].strip()
        self.set_method()
        self.set_status_code()

    def set_new_user(self):
        """
        If no specific user was specified
        Choose a random user for outbound browsing event
        """
        self.current_user = random.choice(self.hosts)

    def set_new_endpoint(self):
        """
        External website user is browsing to

        """
        self.current_endpoint = random.choice(self.endpoints)

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
        logline = ' '.join([str(x) for x in [self.time, self.method, self.src_ip, self.url, self.request, self.dst_ip,
                                             self.user_agent]])

        return logline

    def set_request(self, stringLength=10):
        """
        Generate a random string of fixed length
        thanks to: https://pynative.com/python-generate-random-string/
        """
        letters = string.ascii_lowercase
        extension = random.choice(['.html', '.js', '.css', '.png',
                                   '.jpg', '.exe', '.docx', '.xls', ''])
        self.request = ''.join(
            random.choice(letters) for i in range(stringLength)) + extension
