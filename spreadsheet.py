import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = '1C2oeLma9674aj7hQxmkXxu3dl6jb6coMK8Au_GZ2PSw'  # enter your own here
TAB_NAME = 'sleep'  # enter your own here


## !!! DOWNLOAD THE credentials.json from https://developers.google.com/sheets/api/quickstart/python

def add_rows_to_sleep_tab(rows):
    creds = google_auth()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    append_values(sheet, TAB_NAME, 'USER_ENTERED', rows)


def append_values(sheet, range_name, value_input_option, values):
    body = {
        'values': values
    }
    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID, range=range_name,
        valueInputOption=value_input_option, body=body).execute()
    print('{0} cells appended.'.format(result.get('updates').get('updatedCells')))
    return result


def google_auth():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds
