import os
import hashlib
import tarfile
import boto3

class ObjectStorage:
    def __init__(self, endpoint_url, aws_access_key_id, aws_secret_access_key, aws_session_token, 
                 bucket_name="daytona-volume-builds"):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
        )
    
    def upload(self, path, organization_id, archive_base_path=None, delete_tar=True) -> str:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path does not exist: {path}")
        
        # Compute hash for the path
        path_hash = self._compute_hash_for_path_md5(path, archive_base_path)
        
        # Define the S3 prefix
        prefix = f"{organization_id}/{path_hash}/"
        s3_key = prefix + "context.tar"
        
        # Check if it already exists in S3
        if self._folder_exists_in_s3(prefix):
            return path_hash
        
        # Create tar archive
        tar_file = self._create_tar_uncompressed(path, archive_base_path, tar_path="context.tar")
        
        # Upload to S3
        self.s3_client.upload_file(tar_file, self.bucket_name, s3_key)
        
        # Delete tar file if requested
        if delete_tar:
            os.remove(tar_file)

        return path_hash
    
    def _compute_hash_for_path_md5(self, path_str, archive_base_path=None):
        md5_hasher = hashlib.md5()
        abs_path_str = os.path.abspath(path_str)
        
        if archive_base_path is None:
            archive_base_path = self._compute_archive_base_path(path_str)
        md5_hasher.update(archive_base_path.encode("utf-8"))
        
        if os.path.isfile(abs_path_str):
            with open(abs_path_str, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    md5_hasher.update(chunk)
        else:
            for root, dirs, files in os.walk(abs_path_str):
                if not dirs and not files:
                    rel_dir = os.path.relpath(root, path_str)
                    md5_hasher.update(rel_dir.encode("utf-8"))
                for filename in files:
                    file_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(file_path, abs_path_str)
                    
                    # Incorporate the relative path
                    md5_hasher.update(rel_path.encode("utf-8"))
                    
                    # Incorporate file contents
                    with open(file_path, "rb") as f:
                        for chunk in iter(lambda: f.read(8192), b""):
                            md5_hasher.update(chunk)
        
        return md5_hasher.hexdigest()
    
    def _folder_exists_in_s3(self, prefix):
        resp = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
        return 'Contents' in resp
    
    def _create_tar_uncompressed(self, source_path, archive_base_path=None, tar_path="context.tar"):
        source_path = os.path.normpath(source_path)
        
        if archive_base_path is None:
            archive_base_path = self._compute_archive_base_path(source_path)
        
        with tarfile.open(tar_path, mode="w") as tar:
            tar.add(source_path, archive_base_path)
        return tar_path
    
    @staticmethod
    def _compute_archive_base_path(path_str) -> str:
        path_str = os.path.normpath(path_str)
        # Remove drive letter for Windows paths (e.g., C:)
        _, path_without_drive = os.path.splitdrive(path_str)
        # Remove leading separators (both / and \)
        return path_without_drive.lstrip('/').lstrip('\\')
