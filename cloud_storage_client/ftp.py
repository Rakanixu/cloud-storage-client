import os, sys, tarfile
from shutil import copyfile
from distutils.dir_util import copy_tree
from ftplib import FTP

class FTPClient():
  """
  FTP Client to connect with FTP servers
  """

  def __init__(self, host, port, username, password):
    self.client = FTP()
    self.client.connect(host, port)
    self.client.login(username, password)

  def delete_file(self, file_path):
    if file_path[0] != '/':
      remote_path = '/' + file_path
    else:
      remote_path = file_path
    self.client.delete(remote_path)

  def delete_folder(self, folder_id):
    if folder_id[0] != '/':
      path = '/' + folder_id
    else:
      path = folder_id

    for file in self.client.nlst(path):
      self.client.delete(file)

  def download_folder(self, src_folder, dst_folder):
    if src_folder[0] != '/':
      src_path = '/' + src_folder
    else:
      src_path = src_folder

    os.makedirs(dst_folder, exist_ok=True)
    for f in self.client.nlst(src_folder):
      f_path = f.split('/')
      file_name = f_path[len(f_path) - 1]
      try:
        file = open(dst_folder + '/' + file_name, 'wb+')
        self.client.retrbinary('RETR ' + src_folder + '/' + file_name, file.write)
        file.close()
      except Exception:
        print(src_folder + '/' + file_name + " not a file.")

  def upload_file(self, src_file, dst_file):
    split_dst_file = dst_file.split('/')
    remote_path = ""
    for i in range(len(split_dst_file) - 1):
      remote_path += "/" + split_dst_file[i]
       
    try:
      self.client.cwd(remote_path)
    except:
      for i in range(len(split_dst_file) - 1):
        try:
          self.client.cwd(split_dst_file[i])
        except:
          self.client.mkd(split_dst_file[i])
          self.client.cwd(split_dst_file[i])

    file = open(src_file, 'rb')
    self.client.storbinary('STOR ' + split_dst_file[len(split_dst_file) - 1], file)
    file.close()
    self.client.cwd("/")

  def upload_files(self, folder_id, selected_chunks, folder_chunks, do_tar=False, do_compress=False):
    if folder_id[0] != '/':
      remote_folder = '/' + folder_id
    else:
      remote_folder = folder_id
  
    split_dst_file = remote_folder.split('/')
    remote_path = ""
    for i in range(len(split_dst_file) - 1):
      remote_path += "/" + split_dst_file[i]
       
    try:
      self.client.cwd(remote_path)
    except:
      for i in range(len(split_dst_file) - 1):
        try:
          self.client.cwd(split_dst_file[i])
        except:
          self.client.mkd(split_dst_file[i])
          self.client.cwd(split_dst_file[i])

    if do_tar:
      if do_compress:
        ext = '.tgz'
        verb = 'w:gz'
      else:
        ext = '.tar'
        verb = 'w'

      folder_id_path = folder_id.split('/')
      folder_id_short = folder_id_path[len(folder_id_path) - 1]
      folder = '/tmp/' + folder_id_short

      for chunk in selected_chunks:
        copyfile(folder_chunks + '/' + chunk, folder)        

      folder_compress = '/tmp/' + folder_id_short + ext
      with tarfile.open(folder_compress, verb) as tar:
        tar.add(folder, recursive=True)
      tar.close()
      print(folder_compress, '/' + folder_id + '/' + folder_id_short + ext)

      file = open(folder_compress, 'rb')
      self.client.storbinary('STOR ' + folder_id_short + ext, file)
      file.close()
    else:
      for chunk in selected_chunks:
        file = open(folder_chunks + '/' + chunk, 'rb')
        self.client.storbinary('STOR ' + chunk, file)
        file.close()
    
    self.client.cwd("/")

  def download_file(self, folder_id, selected_chunk, output_folder):
    if folder_id == '':
      file_path = selected_chunk
    else:
      file_path = folder_id + '/' + selected_chunk

    file = open(output_folder + '/' + selected_chunk, 'wb+')
    self.client.retrbinary('RETR ' + file_path, file.write)
    file.close()

  def upload_folder(self, dst_folder, src_folder, do_tar=False, do_compress=False):
    if dst_folder[0] != '/':
      remote_folder = '/' + dst_folder
    else:
      remote_folder = dst_folder
  
    split_dst_file = remote_folder.split('/')
    remote_path = ""
    for i in range(len(split_dst_file) - 1):
      remote_path += "/" + split_dst_file[i]
       
    try:
      self.client.cwd(remote_path)
    except:
      for i in range(len(split_dst_file) - 1):
        try:
          self.client.cwd(split_dst_file[i])
        except:
          self.client.mkd(split_dst_file[i])
          self.client.cwd(split_dst_file[i])

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
      file = open(folder_compress, 'rb')
      self.client.storbinary('STOR ' + 'result' + ext, file)
      file.close()
    else:
      dir = os.fsencode(src_folder)
      for f in os.listdir(dir):
        filePath = src_folder + '/' + f.decode('utf-8')
        if not os.path.isdir(filePath):
          file = open(filePath, 'rb')
          self.client.storbinary('STOR ' + f.decode('utf-8'), file)
          file.close()
    
    self.client.cwd("/")

  def list_files_folder(self, folder):
    if folder[0] != '/':
      remote_folder = '/' + folder
    else:
      remote_folder = folder
    return self.client.nlst(remote_folder)
