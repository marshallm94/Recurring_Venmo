import numpy as np

bills = {'water': {'query': 'Metro Water Services AND new bill',
                   'search_string': '. ',
                   'chargee': '@Emily-Solem',
                   'multiplier': 0.5},
         'electric': {'query': 'from:NES subject:Payment Processed',
                      'search_string': ' ',
                      'chargee': '@Emily-Solem',
                      'multiplier': 0.5},
         'xfinity': {'query': 'from:Xfinity subject:Thank you for your recent payment',
                     'search_string': ' ',
                     'chargee': '@Emily-Solem',
                     'multiplier': 0.5}}

class Bill(object):

    def __init__(self, name, total, date, multiplier, chargee, venmo_command):

        self.name = name
        self.multiplier = multiplier
        self.chargee = chargee
        self.total = total
        self.date = date
        self.venmo_command = venmo_command
        self.amount_to_be_charged = np.round(self.total * self.multiplier, 2)
        self.request_string = self.create_venmo_request()

    def create_venmo_request(self):

        request_string = f"{self.name} bill - {self.date.strftime('%Y-%m-%d')}"
        venmo_CLI_string = f"{self.venmo_command} charge {self.chargee} {self.amount_to_be_charged} '{request_string}'\n"

        return venmo_CLI_string
