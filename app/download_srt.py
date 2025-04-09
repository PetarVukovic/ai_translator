from app.get_creds import getCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import io


async def download_srt():
    creds = getCredentials()
    try:
        service = build("drive", "v3", credentials=creds)
        folder_id = "17Kk7PTqpF6oByALM_nV65SR2T_1QZ_OT"
        request = service.files().get_media(fileId=folder_id)
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
