import requests
from datetime import datetime as dt

from EmailParser import EmailParser 
from Bill import Bill, bills

with open(".last_run_date.txt") as date_file:
    last_run_date = dt.strptime(date_file.readline().strip(), "%Y-%m-%d %H:%M:%S")

with open('.textbelt_api_key.txt') as key:
    api_key = key.readline().strip()

with open('output.log', 'w') as venmo_requests:

    full_text_body = ""
    full_charge_amount = 0
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

                full_text_body += str(bill) + "\n"
                full_charge_amount += bill.amount_to_be_charged

    full_text_body += f"\nTotal = {full_charge_amount}\n"

    request_dict = {'phone': '3038106250', 'message': full_text_body, 'key': api_key}
    resp = requests.post('https://textbelt.com/text/', request_dict)

    log_info = resp.json()


# should be last thing to execute
# with open(".last_run_date.txt", 'w') as date_file:
#     today = dt.strftime(dt.today(), "%Y-%m-%d %H:%M:%S")
#     date_file.write(str(today) + "\n")
