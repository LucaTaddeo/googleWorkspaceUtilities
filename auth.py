import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/admin.directory.user",
    "https://www.googleapis.com/auth/admin.directory.group",
    "https://www.googleapis.com/auth/calendar",
]

creds = None

def loginAndInitializeService():
    global creds
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        print("| Logging in using saved credentials...")

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("| Refreshing your credentials...")
            creds.refresh(Request())
        else:
            print("| Use your browser to login...")
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # Initialize an admin service with given credentials
    print("| Authentication succeeded!")
    return build("admin", "directory_v1", credentials=creds)
