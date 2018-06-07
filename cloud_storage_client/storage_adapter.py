class StorageAdapter:

    def delete_file(self, file_path): pass
    def delete_folder(self, folder_id): pass
    def download_folder(self, src_folder, dst_folder): pass
    def upload_file(self, src_file, dst_file): pass
    def upload_files(self, folder_id, selected_chunks, folder_chunks, do_tar=False, do_compress=False): pass
    def download_file(self, folder_id, selected_chunk, output_folder): pass
    def upload_folder(self, dst_folder, src_folder, do_tar=False, do_compress=False): pass
