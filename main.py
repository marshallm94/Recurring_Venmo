from datetime import datetime as dt

from EmailParser import EmailParser 
from Bill import Bill, bills

with open(".last_run_date.txt") as date_file:
    last_run_date = dt.strptime(date_file.readline().strip(), "%Y-%m-%d %H:%M:%S")

with open(".venmo_path.txt") as venmo_command_file:
    venmo_command = venmo_command_file.readline().strip()

with open('venmo_requests_to_make.sh', 'w') as venmo_requests:

    venmo_requests.write("#!/bin/bash\n\n")

    for bill_name, bill_info in bills.items():
        parser = EmailParser(query = bill_info['query'],
                             search_string = bill_info['search_string'])

        for bill_email in parser.results:
            if bill_email['date'] >= last_run_date:
                bill = Bill(name = bill_name,
                            total = bill_email['total'],
                            date = bill_email['date'],
                            multiplier = bill_info['multiplier'],
                            chargee = bill_info['chargee'])

                venmo_requests.write(bill.create_venmo_request(venmo_command))


# should be last thing to execute
with open(".last_run_date.txt", 'w') as date_file:
    today = dt.strftime(dt.today(), "%Y-%m-%d %H:%M:%S")
    date_file.write(str(today) + "\n")
