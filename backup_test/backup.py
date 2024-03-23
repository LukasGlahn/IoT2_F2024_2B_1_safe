from azure.storage.blob import BlobServiceClient
import shutil
from datetime import datetime
import os
from time import sleep

storage_account_key = ""
storage_account_name = ""
connection_string = ""
container_name = "backup"

def uploadToBlobStorage(file_path,file_name):
   blob_service_client = BlobServiceClient.from_connection_string(connection_string)
   blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
   with open(file_path,'rb') as data:
      blob_client.upload_blob(data)
      print(f'Uploaded {file_name}.')

# calling a function to perform upload
      
# Get the current date and time
time_raw = datetime.now()
time_formatted = f'{time_raw.day}.{time_raw.month}.{time_raw.year}.kl.{time_raw.hour}.{time_raw.minute}'

# Make archive
shutil.make_archive(f'C:\\Users\\lukas\\Desktop\\Programering kea\\2_semester\\IoT2_F2024_2B_1\\IoT2_F2024_2B_1\\backup_test\\backup{time_formatted}', 'zip', 'C:\\Users\\lukas\\Desktop\\Programering kea\\2_semester\\IoT2_F2024_2B_1\\IoT2_F2024_2B_1\\backup_test\\database\\')
uploadToBlobStorage(f'C:\\Users\\lukas\\Desktop\\Programering kea\\2_semester\\IoT2_F2024_2B_1\\IoT2_F2024_2B_1\\backup_test\\backup{time_formatted}.zip',f'backup{time_formatted}.zip')
sleep(3)
os.remove(f'C:\\Users\\lukas\\Desktop\\Programering kea\\2_semester\\IoT2_F2024_2B_1\\IoT2_F2024_2B_1\\backup_test\\backup{time_formatted}.zip')
