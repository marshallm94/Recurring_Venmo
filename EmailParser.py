from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import base64
import email

from datetime import datetime as dt

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
store = file.Storage('.token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('.credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))

class EmailParser(object):

    def __init__(self, query, search_string):

        self.query = query
        self.search_string = search_string
        self.query_matches = self._get_query_results() 
        self.results = []
        self.main()

    def main(self):

        # TODO: is it worth passing the email_id to self.extract_bill_info()
        # as a means of identifying which messages weren't able to parse
        # (i.e. exception handling)?
        for email_id, message_info in self.query_matches.items():

            self.extract_bill_info(message_info)

    def extract_bill_info(self, message):
        '''
        Extracts all the important bill information from an email.

        Parameters:
        ----------
        message : (dict)
            A dictionary that contains the key 'snippet' whose value contains
            all relevant transaction information (date, amount, bill_name).

        Returns:
        ----------
        None (appends small dictionary to self.results with keys 'date' and
        'total')
        '''
        try:
            # get date
            date_value = dt.fromtimestamp(int(message['internalDate'])/1000)

            # get total bill amount
            start_idx = message['snippet'].find('$') + 1
            first_space_idx = message['snippet'][start_idx:-1].find(self.search_string)
            total = float(message['snippet'][start_idx:-1][:first_space_idx])

            self.results.append({'date': date_value, 'total': total})
        except ValueError:
            print("Error parsing email with specified search string.")


    def _get_query_results(self, query = None):
        '''
        Get any messaages that match self.query from your Gmail account.

        Parameters:
        ----------
        query : (str)
            A query that specifies the subset of messages to retrieve. Check
            (https://support.google.com/mail/answer/7190) for valid options. Note
            that these are the same options that one can manually type into the
            search bar withing Gmail.

        Returns:
        ----------
        message_dict : (dict)
            A "dict of dict's," the keys being the massage ID's of messages that
            matched the query, the values being dictionaries containing additional
            message data.
        '''
        if not query:
            query = self.query

        # Call the Gmail API to fetch INBOX
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])

        message_dict = {}
        for message in messages:
            # msg is a dict
            msg = service.users().messages().get(userId='me',id=message['id'],format='raw').execute()

            # removing ID since it will be used as the key for the returned
            # dictionary - adhering to DRY
            del msg['id']
            message_dict[message['id']] = msg

            msg_str = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
            mime_msg = email.message_from_bytes(msg_str)
            email_text = ""
            for part in mime_msg.walk():
                if part.get_content_type() == 'text/plain':
                    email_text += part.get_payload()

            message_dict[message['id']]['email_text'] = email_text

        return message_dict
