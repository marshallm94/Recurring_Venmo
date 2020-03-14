from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import base64
import email
from apiclient import errors

from datetime import datetime as dt

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))
    

def get_query_results(query):
    '''
    Get any messaages that match query from your Gmail account.

    Parameters:
    ----------
    query : (str)
        A query that specifies the subset of messages to retrieve. Check
        (https://support.google.com/mail/answer/7190) for valid options. Note
        that these are the same options that one can manually type into the
        search bar withing Gmail.

    Returns:
    ----------
    out : (dict)
        A "dict of dict's," the keys being the massage ID's of messages that
        matched the query, the values being dictionaries containing additional
        message data.
    '''
    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me',q=query).execute()
    messages = results.get('messages', [])

    out = {}
    for message in messages:
        # msg is a dict
        msg = service.users().messages().get(userId='me',id=message['id'],format='raw').execute()

        # removing ID since it will be used as the key for the returned
        # dictionary - adhering to DRY
        del msg['id']
        out[message['id']] = msg

        msg_str = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
        mime_msg = email.message_from_bytes(msg_str)
        email_text = ""
        for part in mime_msg.walk():
            if part.get_content_type() == 'text/plain':
                email_text += part.get_payload()

        out[message['id']]['email_text'] = email_text

    return out

def extract_electric_bill_info(email_id, message):

    # get total bill amount
    try:
        start_idx = message['snippet'].find('$') + 1
        first_space_idx = message['snippet'][start_idx:-1].find(' ')
        total_amount = float(message['snippet'][start_idx:-1][:first_space_idx])

        # get date
        value = dt.fromtimestamp(int(subdict['internalDate'])/1000)
        email_date = value.strftime("%Y-%m-%d")

        return total_amount, email_date
    except:
        print(f"Something went wrong with the parsing of email with ID {email_id}")

def extract_xfinity_bill_info(email_id, message):

    # get total bill amount
    try:
        start_idx = message['snippet'].find('$') + 1
        first_space_idx = message['snippet'][start_idx:-1].find(' ')
        total_amount = float(message['snippet'][start_idx:-1][:first_space_idx])

        # get date
        value = dt.fromtimestamp(int(subdict['internalDate'])/1000)
        email_date = value.strftime("%Y-%m-%d")

        return total_amount, email_date
    except:
        print(f"Something went wrong with the parsing of email with ID {email_id}")

def extract_water_bill_info(email_id, message):

    # get total bill amount
    try:
        start_idx = message['snippet'].find('$') + 1
        first_space_idx = message['snippet'][start_idx:-1].find('. ')
        total_amount = float(message['snippet'][start_idx:-1][:first_space_idx])

        # get date
        value = dt.fromtimestamp(int(subdict['internalDate'])/1000)
        email_date = value.strftime("%Y-%m-%d")

        return total_amount, email_date
    except:
        print(f"Something went wrong with the parsing of email with ID {email_id}")

def extract_transaction_info(email_id, message, bill_type):
    '''
    Extracts the info necessary for a Venmo request to be sent
    (using the Venmo CLI):

    Parameters:
    ----------
    message : (dict)
        A dictionary that contains the a key 'snippet' whose value contains
        all relevant transaction information (date, amount, bil_typ).

    Returns:
    ----------
    out : (dict)
        A dictionary containing with the keys:
            * 'date'
            * 'total_amount'
            * 'amount_to_be_charged'
            * 'payor'
    '''
    if bill_type == 'xfinity':
        out = extract_xfinity_bill_info(email_id, message)
    elif bill_type == 'water':
        out = extract_water_bill_info(email_id, message)
    elif bill_type == 'electric':
        out = extract_electric_bill_info(email_id, message)

    return out
    
if __name__ == '__main__':
    electric_bill_query = 'from:NES subject:Payment Processed'
    water_bill_query = "Metro Water Services AND new bill"
    xfinity_bill_query = 'from:Xfinity subject:Thank you for your recent payment'

    bills = {'water': water_bill_query,
             'electric': electric_bill_query,
             'xfinity': xfinity_bill_query}
    for bill, query in bills.items():
        results = get_query_results(query)
        for email_id, subdict in results.items():
            print(extract_transaction_info(email_id, subdict, bill))

