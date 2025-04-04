import io
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from get_creds import getCredentials


def download_file(real_file_id):
    """Downloads a file
    Args:
        real_file_id: ID of the file to download
    Returns : IO object with location.
    """
    creds = getCredentials()

    try:
        # create drive api client
        service = build("drive", "v3", credentials=creds)

        file_id = real_file_id

        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}.")

    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None

    return file.getvalue()


def fetch_start_page_token():
    try:
        # create drive api client
        service = build("drive", "v3", credentials=getCredentials())

        # pylint: disable=maybe-no-member
        response = service.changes().getStartPageToken().execute()
        print(f'Start token: {response.get("startPageToken")}')

    except HttpError as error:
        print(f"An error occurred: {error}")
        response = None

    return response.get("startPageToken")


def fetch_changes(start_page_token):
    try:
        # create drive api client
        service = build("drive", "v3", credentials=getCredentials())

        # Begin with our last saved start token for this user or the
        # current token from getStartPageToken()
        page_token = start_page_token
        # pylint: disable=maybe-no-member

        while page_token is not None:
            response = (
                service.changes().list(pageToken=page_token, spaces="drive").execute()
            )
            for change in response.get("changes"):
                # Process change
                print(f'Change found for file: {change.get("fileId")}')
            if "newStartPageToken" in response:
                # Last page, save this token for the next polling interval
                start_page_token = response.get("newStartPageToken")
            page_token = response.get("nextPageToken")

    except HttpError as error:
        print(f"An error occurred: {error}")
        start_page_token = None

    return start_page_token


if __name__ == "__main__":
    path = "/Users/petarvukovic/Desktop/Misija/AI_Translator/srt_files"
    if not os.path.exists(path):
        os.mkdir(path)
    srt_text = download_file(real_file_id="19fMvFyfffbHXwcFN5d-LGTqrpDp_J8D_").decode(
        "utf-8"
    )
    with open(f"{path}/manna4.srt", "w", encoding="utf-8") as f:
        f.write(srt_text)
    page_token = fetch_start_page_token()
    print(page_token)
    fetch_changes(page_token)
