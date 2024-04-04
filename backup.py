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