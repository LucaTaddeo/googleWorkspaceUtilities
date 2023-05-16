# Google Workspace Utilities
Utility Repo containing helper functions for Google Workspace, using the Workspace SDK for Python

## Authentication
The functionality of this application requires authentication. To set it up, follow the steps in the following paragraphs.

### OAuth 2.0
The core functionalities of the applciation, relies on OAuth 2.0 and desktop application credentials. To set it up:
1. [Set up OAuth 2.0 Client ID](https://developers.google.com/calendar/api/quickstart/python#authorize_credentials_for_a_desktop_application)
2. Download the credential file and save it in `credentials/oAuth_credentials.json`

### Service Account
Some functionalities require to work with delegated credentials. In order to do so, follow these steps:
1. [Create a Service Account in Google Cloud](https://developers.google.com/workspace/guides/create-credentials#create_a_service_account)
2. [Set up the domain-wide delegation for the service account](https://developers.google.com/workspace/guides/create-credentials#optional_set_up_domain-wide_delegation_for_a_service_account)
3. [Create the credentials for the Service Account](https://developers.google.com/workspace/guides/create-credentials#create_credentials_for_a_service_account) and save them in `credentials/service_account_credentials.json`