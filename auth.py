import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2 import service_account

from constants import defaultEmail
from utils import getColoredText

SCOPES = [
    "https://www.googleapis.com/auth/admin.directory.user",
    "https://www.googleapis.com/auth/admin.directory.group",
    "https://www.googleapis.com/auth/calendar",
]

creds = None

def loginWithOAuthToken(serviceName, serviceVersion):
    global creds
    if os.path.exists("credentials/token.json"):
        creds = Credentials.from_authorized_user_file("credentials/token.json", SCOPES)
        print("| Logging in for "+serviceName+" using saved credentials...")

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("| Refreshing your credentials")
            creds.refresh(Request())
        else:
            print("| Use your browser to login")
            flow = InstalledAppFlow.from_client_secrets_file("credentials/oAuth_credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("credentials/token.json", "w") as token:
            token.write(creds.to_json())

    # Initialize an admin service with given credentials
    print("| "+getColoredText("OAauth2 Authentication for "+serviceName+ getColoredText(" succeeded!", "bold"), ["green"]))
    return build(serviceName, serviceVersion, credentials=creds)


def loginWithDomainLevelServiceAccount(serviceName, serviceVersion, email=defaultEmail):
    print("| Logging in for "+serviceName+" using service account credentials...")
    credentials = service_account.Credentials.from_service_account_file(
        "credentials/serviceAccount_credentials.json", scopes=SCOPES)
    delegated_credentials = credentials.with_subject(email) 
    print("| Creating delegated credentials for "+email)
    try: 
        delegated_user = build(serviceName, serviceVersion, credentials=delegated_credentials)
        if delegated_user is None:
            raise Exception("Delegated credentials for "+email+" failed!")
        print("| "+getColoredText("Delegated credentials for "+email+ getColoredText(" created!", "bold"), ["green"]))
        print("| ")
        return delegated_user
    except: 
        print("| "+getColoredText("Delegated credentials for "+email+ getColoredText(" failed!", "bold"), ["red"]))
        print("| ")
        return None