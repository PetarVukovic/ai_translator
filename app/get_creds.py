import os.path
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/drive"]


def find_file_in_workspace(file_name: str, workspace_path=".") -> str:
    for root, dirs, files in os.walk(workspace_path):
        if file_name in files:
            return os.path.join(root, file_name)
    return None


def getCredentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if find_file_in_workspace("token.json"):
        creds = Credentials.from_authorized_user_file(
            find_file_in_workspace("token.json"), SCOPES
        )
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                find_file_in_workspace("credentials.json"), SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(find_file_in_workspace("token.json"), "w") as token:
            token.write(creds.to_json())
    return creds
