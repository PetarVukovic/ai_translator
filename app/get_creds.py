import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Scopes – ovdje dodaj sve što ti treba (Drive, Sheets itd.)
SCOPES = ["https://www.googleapis.com/auth/drive"]


def find_file_in_workspace(file_name: str, workspace_path=None) -> str:
    """
    Pretražuje projektni direktorij i njegove podfoldere za traženi fajl.
    Ako workspace_path nije zadan, automatski se ide jedan nivo iznad trenutne skripte.
    """
    if workspace_path is None:
        current_dir = (
            os.path.dirname(os.path.abspath(__file__))
            if "__file__" in globals()
            else os.getcwd()
        )
        workspace_path = os.path.abspath(os.path.join(current_dir, ".."))

    for root, dirs, files in os.walk(workspace_path):
        if file_name in files:
            full_path = os.path.join(root, file_name)
            print(f"✅ Našao sam fajl: {full_path}")
            return full_path

    print(f"❌ Nije pronađen fajl: {file_name}")
    return None


def getCredentials(workspace_path=".."):
    creds = None
    token_path = find_file_in_workspace("token.json", workspace_path=workspace_path)
    creds_path = find_file_in_workspace(
        "credentials.json", workspace_path=workspace_path
    )

    if creds_path is None:
        raise FileNotFoundError(
            "⚠️ 'credentials.json' nije pronađen – provjeri workspace_path!"
        )

    # Ako postoji token i valjan je
    if token_path and os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # Ako nema (ili je expired), pokrećemo flow za novo odobrenje
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Ako token_path nije postojao, kreiraj default lokaciju
        if not token_path:
            token_path = os.path.join(os.path.dirname(creds_path), "token.json")

        with open(token_path, "w") as token:
            token.write(creds.to_json())
            print(f"💾 Token spremljen u: {token_path}")

    return creds


if __name__ == "__main__":
    creds = getCredentials()
    print("🔐 Credentials valid:", creds.valid)
