from azure.storage.common import CloudStorageAccount
from azure.storage.blob import BlockBlobService
from shutil import copyfile
import os, sys, tarfile

class AzureClient():
    """
    Azure Blob Storage Client to connect with Microsoft Azure
    """
    def __init__(self, bucket_name, access_key, secret_key):
        self.service = BlockBlobService(account_name=access_key, account_key=secret_key)
        self.bucket_name = bucket_name

    def delete_file(self, file_path):
        if file_path[0] == '/':
            file_path = file_path[1:len(file_path)]
        self.service.delete_blob(self.bucket_name, file_path)
        
    def delete_folder(self, folder_id):
        blobs = self.service.list_blobs(self.bucket_name)
        if folder_id[0] == '/':
            folder_id = folder_id[1:len(folder_id)]
        for blob in blobs:
            if blob.name.find(folder_id + '/') == 0:
                self.service.delete_blob(self.bucket_name, blob.name)
                
    def download_folder(self, src_folder, dst_folder):
        blobs = self.service.list_blobs(self.bucket_name)
        if src_folder[0] == '/':
            src_folder = src_folder[1:len(src_folder)]
        for blob in blobs:
            if blob.name.find(src_folder + '/') == 0:
                if not os.path.exists(dst_folder):
                    os.makedirs(dst_folder)
                splitted_name = blob.name.split('/')
                self.service.get_blob_to_path(self.bucket_name, blob.name, dst_folder + '/' + splitted_name[len(splitted_name) - 1])

    def upload_file(self, src_file, dst_file):
        if dst_file[0] == '/':
            dst_file = dst_file[1:len(dst_file)]    
        if dst_file[-1] == '/':
            dst_file = dst_file[0:len(dst_file) - 1]
        dst_file = dst_file.replace('//', '/')            

        self.service.create_blob_from_path(self.bucket_name, dst_file, src_file)

    def upload_files(self, folder_id, selected_chunks, folder_chunks, do_tar=False, do_compress=False):
        print('DoTar {}, DoCompress {}'.format(do_tar, do_compress))
        if folder_id[0] == '/':
            folder_id = folder_id[1:len(folder_id)] 
        if folder_id[-1] == '/':
            folder_id = folder_id[0:len(folder_id) - 1]
        folder_id = folder_id.replace('//', '/')

        if do_tar:
            if do_compress:
                ext = '.tgz'
                verb = 'w:gz'
            else:
                ext = '.tar'
                verb = 'w'

            folder = '/tmp/' + folder_id
            for chunk in selected_chunks:
                copyfile(folder_chunks + '/' + chunk, folder)

            folder_compress = '/tmp/' + folder_id + ext
            with tarfile.open(folder_compress, verb) as tar:
                tar.add(folder, recursive=True)
            tar.close()
            self.service.create_blob_from_path(self.bucket_name, folder_id + '/' + folder_id + ext, folder_compress)
        else:
            for chunk in selected_chunks:            
                self.service.create_blob_from_path(self.bucket_name, folder_id + '/' + chunk, folder_chunks + '/' + chunk)
    
    def download_file(self, folder_id, selected_chunk, output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        if folder_id == '':
            file_path = selected_chunk
        else:
            file_path = folder_id + '/' + selected_chunk
        if file_path[0] == '/':
            file_path = file_path[1:len(file_path)]
        self.service.get_blob_to_path(self.bucket_name, file_path, output_folder + '/' + selected_chunk)

    def upload_folder(self, dst_folder, src_folder, do_tar=False, do_compress=False):
        print('DoTar {}, DoCompress {}'.format(do_tar, do_compress))
        if dst_folder[0] == '/':
            dst_folder = dst_folder[1:len(dst_folder)]
        if do_tar:
            if do_compress:
                ext = '.tgz'
                verb = 'w:gz'
            else:
                ext = '.tar'
                verb = 'w'

            local_folder = '/tmp/{}'.format(dst_folder)
            os.makedirs(local_folder, exist_ok=True)

            folder_compress = '{}/result.{}'.format(local_folder, ext)
            print('Compressing to {}'.format(folder_compress))
            with tarfile.open(folder_compress, verb) as tar:
                tar.add(src_folder, arcname=dst_folder, recursive=True)
            tar.close()
            self.service.create_blob_from_path(self.bucket_name, dst_folder + ext, folder_compress)
        else:
            dir = os.fsencode(src_folder)
            for file in os.listdir(dir):
                filePath = src_folder + '/' + file.decode('utf-8')
                if not os.path.isdir(filePath):
                    self.service.create_blob_from_path(self.bucket_name, dst_folder + '/' + file.decode('utf-8'), filePath)

    def list_files_folder(self, folder):
        blobs = self.service.list_blobs(self.bucket_name)
        if folder[0] == '/':
            folder = folder[1:len(folder)]
        return [blob.name for blob in blobs if blob.name.find(folder + '/') == 0]

