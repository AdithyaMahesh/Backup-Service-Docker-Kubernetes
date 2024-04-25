import os
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Starting backup process.')
try:
    # Backup logic here
    logging.info('Backup completed successfully.')
except Exception as e:
    logging.error(f'Backup failed: {str(e)}')

# Path to service account key file
SERVICE_ACCOUNT_FILE = r"D:\CS\CloudComputing\GoogleCloud\cloud-computing-project-sem6-5f1315064210.json"

# Scopes required by our application
SCOPES = ['https://www.googleapis.com/auth/drive']

def gdrive_service():
    """
    Authenticate using the service account file and return the Google Drive service object.
    """
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    service = build('drive', 'v3', credentials=credentials, cache_discovery=False)
    return service

def upload_files(service, folder_path, drive_folder_id):
    """
    Upload files to the specified Google Drive folder.

    :param service: Authenticated Google Drive service object.
    :param folder_path: Path to the local folder containing files to upload.
    :param drive_folder_id: ID of the Google Drive folder where files will be uploaded.
    """
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            file_metadata = {'name': file_name, 'parents': [drive_folder_id]}
            media = MediaFileUpload(file_path, resumable=True)
            try:
                file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                logging.info(f'Uploaded {file_name} to Google Drive with ID: {file.get("id")}')
            except Exception as e:
                logging.error(f'Failed to upload {file_name} due to {e}')
        else:
            logging.info(f'Skipped {file_name}, not a file.')

if __name__ == '__main__':
    # Environment variables to specify local folder path and Google Drive folder ID
    folder_path = os.getenv('LOCAL_FOLDER_PATH', r'D:\College\Sem6\CC\project\testing')
    drive_folder_id = os.getenv('DRIVE_FOLDER_ID', '1etWhcZin1hTQYgYuhEJJbZanw7Ii3d9f')
    
    # Initializing the Google Drive service object using the service account
    service = gdrive_service()
    
    # Upload files from the specified local folder to the specified Google Drive folder
    upload_files(service, folder_path, drive_folder_id)
