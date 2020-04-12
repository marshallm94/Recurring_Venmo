import numpy as np

class Bill(object):

    def __init__(self, name, total, multiplier, chargee):

        self.name = name
        self.multiplier = multiplier
        self.chargee = chargee
        self.total = total
        self.amount_to_be_charged = np.round(self.total * self.multiplier, 2)
        self.request_string = self.create_venmo_request()

    def create_venmo_request(self):

        request_string = f"{self.name} bill - {date.strftime('%Y-%m-%d')}"
        venmo_CLI_string = f"venmo charge {self.chargee} {self.amount_to_be_charged} '{request_string}'\n"

        return venmo_CLI_string


