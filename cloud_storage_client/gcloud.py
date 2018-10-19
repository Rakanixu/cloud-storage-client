import os, sys, tarfile
from shutil import copyfile
from google.cloud import storage

CHUNK_SIZE = 10485760

class GCloudStorageClient():
    """
    Google Cloud Storage Client to connect with Goocle Cloud Storage
    """

    def __init__(self, bucket_name):
        self.client = storage.Client()
        self.bucket_name = bucket_name

    def delete_file(self, file_path):
        bucket = self.client.get_bucket(self.bucket_name)
        if file_path[0] == '/':
            file_path = file_path[1:len(file_path)]
        blobs = bucket.list_blobs(prefix=file_path)

        for blob in blobs:
            if blob.name.find(file_path) == 0:
                blob = bucket.blob(blob.name, chunk_size=CHUNK_SIZE)
                blob.delete()

    def delete_folder(self, folder_id):
        bucket = self.client.get_bucket(self.bucket_name)
        if folder_id[0] == '/':
            folder_id = folder_id[1:len(folder_id)]
        blobs = bucket.list_blobs(prefix=folder_id)

        for blob in blobs:
            if blob.name.find(folder_id + '/') == 0:
                blob = bucket.blob(blob.name, chunk_size=CHUNK_SIZE)
                blob.delete()

    def download_folder(self, src_folder, dst_folder):
        bucket = self.client.get_bucket(self.bucket_name)
        if src_folder[0] == '/':
            foldersrc_folder_id = src_folder[1:len(src_folder)]
        blobs = bucket.list_blobs(prefix=src_folder)

        for blob in blobs:
            if blob.name.find(src_folder + '/') == 0:
                if not os.path.exists(dst_folder):
                    os.makedirs(dst_folder)
                splitted_name = blob.name.split('/')
                blob.download_to_filename(dst_folder + '/' + splitted_name[len(splitted_name) - 1])

    def upload_file(self, src_file, dst_file):
        bucket = self.client.get_bucket(self.bucket_name)
        if dst_file[0] == '/':
            dst_file = dst_file[1:len(dst_file)]
        if dst_file[-1] == '/':
            dst_file = dst_file[0:len(dst_file) - 1]
        dst_file = dst_file.replace('//', '/')            

        blob = bucket.blob(dst_file, chunk_size=CHUNK_SIZE)
        blob.cache_control = 'public, max-age=2'
        blob.upload_from_filename(filename=src_file)

    def upload_files(self, folder_id, selected_chunks, folder_chunks, do_tar=False, do_compress=False):
        bucket = self.client.get_bucket(self.bucket_name)
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
            blob = bucket.blob(folder_id + '/' + folder_id + ext, chunk_size=CHUNK_SIZE)
            blob.cache_control = 'public, max-age=2'
            blob.upload_from_filename(filename=folder_compress)
        else:
            for chunk in selected_chunks:
                blob = bucket.blob(folder_id + '/' + chunk, chunk_size=CHUNK_SIZE)
                blob.cache_control = 'public, max-age=2'
                blob.upload_from_filename(filename=folder_chunks + '/' + chunk)

    def download_file(self, folder_id, selected_chunk, output_folder):
        bucket = self.client.get_bucket(self.bucket_name)
        if folder_id == '':
            file_path = selected_chunk
        else:
            file_path = folder_id + '/' + selected_chunk
        if file_path[0] == '/':
            file_path = file_path[1:len(file_path)]
        blob = bucket.blob(file_path, chunk_size=CHUNK_SIZE)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        splitted_name = blob.name.split('/')
        blob.download_to_filename(output_folder + '/' + splitted_name[len(splitted_name) - 1])

    def upload_folder(self, dst_folder, src_folder, do_tar=False, do_compress=False):
        bucket = self.client.get_bucket(self.bucket_name)
        if dst_folder[0] == '/':
            dst_folder = dst_folder[1:len(dst_folder)]
        print('DoTar {}, DoCompress {}'.format(do_tar, do_compress))
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
            blob = bucket.blob(dst_folder + ext, chunk_size=CHUNK_SIZE)
            blob.cache_control = 'public, max-age=2'
            blob.upload_from_filename(filename=folder_compress)
        else:
            dir = os.fsencode(src_folder)
            for file in os.listdir(dir):
                filePath = src_folder + '/' + file.decode('utf-8')
                if not os.path.isdir(filePath):
                    blob = bucket.blob(dst_folder + '/' + file.decode('utf-8'), chunk_size=CHUNK_SIZE)
                    blob.cache_control = 'public, max-age=2'
                    blob.upload_from_filename(filename=filePath)

    def list_files_folder(self, folder):
        bucket = self.client.get_bucket(self.bucket_name)
        if folder[0] == '/':
            folder = folder[1:len(folder)]
        return [blob.name for blob in bucket.list_blobs(prefix=folder) if blob.name.find(folder + '/') == 0]

