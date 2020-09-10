import numpy as np

bills = {'water': {'query': 'Metro Water Services AND new bill',
                   'search_string': '. ',
                   'multiplier': 0.5},
         'electric': {'query': 'from:NES subject:Payment Processed',
                      'search_string': ' ',
                      'multiplier': 0.5},
         'xfinity': {'query': 'from:Xfinity subject:Thank you for your recent payment',
                     'search_string': ' ',
                     'multiplier': 0.5}}

class Bill(object):

    def __init__(self, name, total, date, multiplier):

        self.name = name
        self.multiplier = multiplier
        self.total = total
        self.date = date
        self.amount_to_be_charged = np.round(self.total * self.multiplier, 2)

    def __str__(self):

        info_string = f"{self.name} bill | {self.date.strftime('%Y-%m-%d')} | {self.amount_to_be_charged} ({self.multiplier * 100}%)"

        return info_string
