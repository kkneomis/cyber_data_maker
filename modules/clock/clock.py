from datetime import datetime
from datetime import timedelta
import random


class Clock:
    """
    Time class allows all events to be on the
    same schedule
    """

    def __init__(self, start, interval):
        self.current_time = start
        self.interval = interval

    def tick(self):
        self.current_time += timedelta(
            seconds=random.randint(0, self.interval))

    def get_time(self):
        return self.current_time

    def print_time(self):
        print("<Current time is... %s>" % self.current_time)
