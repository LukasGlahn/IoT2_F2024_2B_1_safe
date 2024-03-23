from azure.storage.blob import BlobServiceClient
import shutil
from datetime import datetime
import os
from time import sleep
import schedule


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
      

def make_backup():
   time_raw = datetime.now()
   time_formatted = f'{time_raw.day}.{time_raw.month}.{time_raw.year}.kl.{time_raw.hour}.{time_raw.minute}'
   shutil.make_archive(f'/home/lukasglahn/Desktop/Iot2{time_formatted}', 'zip', '/home/lukasglahn/Desktop/Iot2/database/')
   uploadToBlobStorage(f'/home/lukasglahn/Desktop/Iot2{time_formatted}.zip',f'backup{time_formatted}.zip')
   sleep(3)
   os.remove(f'/home/lukasglahn/Desktop/Iot2{time_formatted}.zip')
   print('Backup compleet')
   return


schedule.every().day.at("18:00").do(make_backup)

print('im alive')
while True:
    schedule.run_pending()
    sleep(60) # wait one minute