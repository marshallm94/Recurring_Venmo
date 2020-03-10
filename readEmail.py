from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import base64
import email
from apiclient import errors

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))
    

def get_query_results(query):
   
    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me',q=query).execute()
    messages = results.get('messages', [])

    out = {}
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        out[message['id']] = msg

    return out
    
# NOTE(mmcquillen): below function directly from documentation at:
# https://developers.google.com/gmail/api/v1/reference/users/messages/get
def GetMimeMessage(msg_id, service=service, user_id='me'):
    """Get a Message and use it to create a MIME Message.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        msg_id: The ID of the Message required.

    Returns:
        A MIME Message, consisting of data from Message.

    """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()
        print(f "Message snippet: {message['snippet']}" )

        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        mime_msg = email.message_from_string(msg_str)
        return mime_msg

    except errors.HttpError:
        print(f 'An error occurred: {error}' )


if __name__ == '__main__':
    electric_bill_query = 'from:NES subject:Payment Processed'
    water_bill_query = "Metro Water Services AND new bill"
    xfinity_bill_query = 'from:Xfinity subject:recent payment'

    results = get_query_results(xfinity_bill_query)
    for msg in results.values():
        print(msg['snippet'])
        print('\n')
