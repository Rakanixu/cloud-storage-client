from cloud_storage_client import storage_adapter
from cloud_storage_client import gcloud
from cloud_storage_client import as3
from cloud_storage_client import azure
from cloud_storage_client import sftp
from cloud_storage_client import ftp
from cloud_storage_client import file_system
import time

GOOGLE_CLOUD_STORAGE = 'GCS'
AMAZON_S3 = 'S3'
AZURE_BLOB_STORAGE = 'ABS'
FTP = 'FTP'
FILE_SYSTEM = 'FILE_SYSTEM'

class StorageClient(storage_adapter.StorageAdapter):

    def __init__(self, type=None, bucket_name=None, access_key=None, secret_key=None, username=None, password=None, host=None, port=None, secure=None):
        if type == GOOGLE_CLOUD_STORAGE:
            self.client = gcloud.GCloudStorageClient(bucket_name)
        elif type == AMAZON_S3:
            self.client = as3.AS3Client(bucket_name, access_key, secret_key, host, secure)
        elif type == AZURE_BLOB_STORAGE:
            self.client = azure.AzureClient(bucket_name, access_key, secret_key)
        elif type == FTP:
            if secure or secure == 'true' or secure == 'True':
                self.client = sftp.SFTPClient(host, port, username, password)
            else:
                self.client = sftp.FTPClient(host, port, username, password)
        elif type == FILE_SYSTEM:
            self.client = file_system.FileSystemClient()
        else:
            raise NameError('Invalid Storage Type')
        
        self.bucket_name = bucket_name

    def delete_file(self, file_path):
        ts = time.time()
        self.client.delete_file(file_path)
        print('Delete file elapsed time', self.elapsed_time(ts, time.time()), ' seconds')

    def delete_folder(self, folder_id):
        ts = time.time()
        self.client.delete_folder(folder_id)
        print('Delete folder elapsed time', self.elapsed_time(ts, time.time()), ' seconds')

    def download_folder(self, src_folder, dst_folder):
        ts = time.time()
        self.client.download_folder(src_folder, dst_folder)
        print('Download folder elapsed time', self.elapsed_time(ts, time.time()), ' seconds')

    def upload_file(self, src_file, dst_file):
        ts = time.time()
        self.client.upload_file(src_file, dst_file)
        print('Upload file elapsed time', self.elapsed_time(ts, time.time()), ' seconds')

    def upload_files(self, folder_id, selected_chunks, folder_chunks, do_tar=False, do_compress=False):
        ts = time.time()
        self.client.upload_files(folder_id, selected_chunks, folder_chunks, do_tar, do_compress)
        print('Upload files elapsed time', self.elapsed_time(ts, time.time()), ' seconds')

    def download_file(self, folder_id, selected_chunk, output_folder):
        ts = time.time()
        self.client.download_file(folder_id, selected_chunk, output_folder)
        print('Download file elapsed time', self.elapsed_time(ts, time.time()), ' seconds')

    def upload_folder(self, dst_folder, src_folder, do_tar=False, do_compress=False):
        ts = time.time()
        self.client.upload_folder(dst_folder, src_folder, do_tar, do_compress)
        print('Upload folder elapsed time', self.elapsed_time(ts, time.time()), ' seconds')

    def list_files_folder(self, folder):
        ts = time.time()
        files = self.client.list_files_folder(folder)
        print('Upload folder elapsed time', self.elapsed_time(ts, time.time()), ' seconds')
        return files

    def elapsed_time(self, init_time, end_time):
        return (int(end_time) - int(init_time))