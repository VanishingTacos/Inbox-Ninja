import os
import time
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://mail.google.com/']

def authenticate_gmail():
    """Authenticate and return a Gmail API service instance."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        # Handle errors from Gmail API.
        print(f'An error occurred: {error}')

def delete_emails(service, sender_email):
    """Delete emails from the specified sender."""
    try:
        # Get the list of messages from the specified sender
        results = service.users().messages().list(userId='me', q=f'from:{sender_email}').execute()
        messages = results.get('messages', [])
        
        if not messages:
            print(f'No emails found from {sender_email}')
            return
        
        for message in messages:
            msg_id = message['id']
            service.users().messages().delete(userId='me', id=msg_id).execute()
            print(f'Deleted email with ID: {msg_id}')
            
    except HttpError as error:
        print(f'An error occurred: {error}')

def main():
    service = authenticate_gmail()
    sender_emails = ['example1@example.com', 'example2@example.com']  # Add more email addresses as needed

    while True:
        for sender_email in sender_emails:
            delete_emails(service, sender_email)
        # Sleep for a specified time before running again (e.g., 60 seconds)
        time.sleep(60)

if __name__ == '__main__':
    main()
