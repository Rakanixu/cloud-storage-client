Intall 

````
pip3 install cloud-storage-client

````



Example usage:

````
from cloud_storage_client import storage
import os

storageClient = storage.StorageClient(
    os.environ['STORAGE_PROVIDER'], # GOOGLE_CLOUD_STORAGE = 'GCS', AMAZON_S3 = 'S3', AZURE_BLOB_STORAGE = 'ABS'
    os.environ['STORAGE_BUCKET_NAME'],
    os.getenv('STORAGE_ACCESS_KEY'),
    os.getenv('STORAGE_SECRET_KEY'))

# Delete single file
storageClient.delete_file('path/file.py')

# Delete a virtual folder
storageClient.delete_folder('path')

# Download a folder
storageClient.download_folder('folder_destination_name', '/Users/user/Downloads')

# Upload a local file
storageClient.upload_file('/Users/user/Documents/my-file.yaml', 'my-file.yaml')

# Download single file
storageClient.download_file('virtual_path', 'file.py', '/Users/user/Documents')

# Upload a folder
storageClient.upload_folder('folder_destination_name', '/Users/user/Documents', do_tar=False, do_compress=False)

# Upload local files
storageClient.upload_files('folder_destination_name', ['file01.py', 'file02.py'], '/Users/user/Documents', do_tar=False, do_compress=False)   

# List remote files over a virtual path / directory
storageClient.list_files_folder('folder_destination_name')

````