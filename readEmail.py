from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

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
        out[message['id']] = msg['snippet']

    return out
    

if __name__ == '__main__':
    electric_bill_query = 'from:NES subject:Payment Processed'
    water_bill_query = "Metro Water Services AND new bill"
    xfinity_bill_query = 'from:Xfinity subject:recent payment'

    results = get_query_results(xfinity_bill_query)
    for msg in results.values():
        print(msg)
        print('\n')
