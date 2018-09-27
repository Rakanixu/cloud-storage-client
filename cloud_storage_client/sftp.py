import os, sys, tarfile
from shutil import copyfile
from distutils.dir_util import copy_tree
import pysftp

class SFTPClient():
  """
  SFTP Client to connect with SFTP servers
  """

  def __init__(self, host, port, username, password):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None 
    self.client = pysftp.Connection(host=host, port=port, username=username, password=password, cnopts=cnopts)

  def delete_file(self, file_path):
    if file_path[0] != '/':
      remote_path = '/' + file_path
    else:
      remote_path = file_path
    self.client.remove(remote_path)
        
  def delete_folder(self, folder_id):
    if folder_id[0] != '/':
      path = '/' + folder_id
    else:
      path = folder_id
    self.client.execute('rm -rf ' + path)

  def download_folder(self, src_folder, dst_folder):
    if src_folder[0] != '/':
      src_path = '/' + src_folder
    else:
      src_path = src_folder
    self.client.get_r(src_path, dst_folder)
    split_src_path = src_path.split('/')
    copy_tree(dst_folder + '/' + src_path, dst_folder + '/' + split_src_path[len(split_src_path) - 1])

  def upload_file(self, src_file, dst_file):
    split_dst_file = dst_file.split('/')
    remote_path = ""
    for i in range(len(split_dst_file) - 1):
      remote_path += "/" + split_dst_file[i]
       
    if not self.client.isdir(remote_path):
      self.client.makedirs(remote_path)

    self.client.put(src_file, dst_file)

  def upload_files(self, folder_id, selected_chunks, folder_chunks, do_tar=False, do_compress=False):
    if folder_id[0] != '/':
      remote_folder = '/' + folder_id
    else:
      remote_folder = folder_id
  
    if not self.client.isdir(remote_folder):
      self.client.makedirs(remote_folder)

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
      print(folder_compress, '/' + folder_id + '/' + folder_id + ext)
      self.client.put(folder_compress, folder_id + '/' + folder_id + ext)
    else:
      for chunk in selected_chunks:
        self.client.put(folder_chunks + '/' + chunk, folder_id + '/' + chunk)

  def download_file(self, folder_id, selected_chunk, output_folder):
    if folder_id == '':
      file_path = selected_chunk
    else:
      file_path = folder_id + '/' + selected_chunk
    self.client.get(file_path, output_folder + '/' + selected_chunk)

  def upload_folder(self, dst_folder, src_folder, do_tar=False, do_compress=False):
    if dst_folder[0] != '/':
      remote_folder = '/' + dst_folder
    else:
      remote_folder = dst_folder
  
    if not self.client.isdir(remote_folder):
      self.client.mkdir(remote_folder)

    print('DoTar {}, DoCompress {}'.format(do_tar, do_compress))
    if do_tar:
      if do_compress:
        ext = '.tgz'
        verb = 'w:gz'
      else:
        ext = '.tar'
        verb = 'w'

      folder_compress = '/tmp/result{}'.format(ext)
      print('Compressing to {}'.format(folder_compress))
      with tarfile.open(folder_compress, verb) as tar:
        tar.add(src_folder, arcname=dst_folder, recursive=True)
      tar.close()
      self.client.put(folder_compress, dst_folder + '/result' + ext)
    else:
      dir = os.fsencode(src_folder)
      for file in os.listdir(dir):
        filePath = src_folder + '/' + file.decode('utf-8')
        if not os.path.isdir(filePath):
          self.client.put(filePath, dst_folder + '/' + file.decode('utf-8'))

  def list_files_folder(self, folder):
    if folder[0] != '/':
      remote_folder = '/' + folder
    else:
      remote_folder = folder
    return self.client.listdir(remote_folder)
