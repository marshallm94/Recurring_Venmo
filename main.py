from EmailParser import EmailParser 
from Bill import Bill

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

with open("last_run_date.txt") as date_file:
    last_run_date = dt.strptime(date_file.readline().strip(), "%Y-%m-%d")


with open('venmo_requests_to_make.sh', 'w') as venmo_requests:

    venmo_requests.write("#!/bin/bash\n\n")

    for bill_name, bill_info in bills.items():
        parser = EmailParser(query = bill_info['query'],
                             search_string = bill_info['search_string'])

        for bill_email in parser.results:
            bill = Bill(name = bill_name,
                        total = bill_email['total'],
                        multiplier = bill_info['multiplier'],
                        chargee = bill_info['chargee'])

            if bill['date'] >= last_run_date:
                venmo_requests.write(bill.request_string)

# should be last thing to execute
with open("last_run_date.txt", 'w') as date_file:
    today = dt.today()
    date_file.write(str(today) + "\n")
