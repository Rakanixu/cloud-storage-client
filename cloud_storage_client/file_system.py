from shutil import copyfile
from distutils.dir_util import copy_tree
import os, sys, tarfile, shutil

class FileSystemClient():
    """
    File System Client 
    """
    def delete_file(self, file_path):
        os.remove(file_path)
        
    def delete_folder(self, folder_id):
        shutil.rmtree(folder_id, True)
                
    def download_folder(self, src_folder, dst_folder):
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)
        copy_tree(src_folder, dst_folder)
    
    def upload_file(self, src_file, dst_file):
        shutil.copyfile(src_file, dst_file)

    def upload_files(self, folder_id, selected_chunks, folder_chunks, do_tar=False, do_compress=False):
        print('DoTar {}, DoCompress {}'.format(do_tar, do_compress))
        if not os.path.exists(folder_id):
            os.makedirs(folder_id)

        if do_tar:
            if do_compress:
                ext = '.tgz'
                verb = 'w:gz'
            else:
                ext = '.tar'
                verb = 'w'

            folder_tmp = '/tmp/' + folder_id
            if not os.path.exists(folder_tmp):
                os.makedirs(folder_tmp)

            for chunk in selected_chunks:
                shutil.copy2(folder_chunks + '/' + chunk, folder_tmp)

            folder_compress = folder_tmp + ext
            print(folder_compress)
            with tarfile.open(folder_compress, verb) as tar:
                tar.add(folder_tmp, recursive=True)
            tar.close() 
            shutil.copyfile(folder_compress, folder_id + ext)
        else:
            for chunk in selected_chunks:
                shutil.copyfile(folder_chunks + '/' + chunk, folder_id + '/' + chunk)

    def download_file(self, folder_id, selected_chunk, output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        if folder_id == '':
            file_path = selected_chunk
        else:
            file_path = folder_id + '/' + selected_chunk
        shutil.copyfile(file_path, output_folder + '/' + selected_chunk)

    def upload_folder(self, dst_folder, src_folder, do_tar=False, do_compress=False):
        print('DoTar {}, DoCompress {}'.format(do_tar, do_compress))
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)

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
            shutil.copyfile(folder_compress, dst_folder + ext)
        else:
            copy_tree(src_folder, dst_folder)

    def list_files_folder(self, folder):
        return os.listdir(folder)

