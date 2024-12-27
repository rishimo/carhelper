from logging import get_logger
from typing import Optional

import minio
from fastapi import UploadFile

from server import CONFIG

logger = get_logger(__name__)


class MinioClient:
    """Minio client."""

    def __init__(self):
        self.client = None

        self._get_minio_client()
        self._check_bucket()

    def _get_minio_client(self):
        """Initialize the Minio client."""

        if self.client is None:
            self.client = minio.Minio(
                CONFIG.minio_endpoint, CONFIG.minio_access_key, CONFIG.minio_secret_key
            )
        logger.info("Minio client initialized")

    def _check_bucket(self):
        """Check if the configured exists and create it if it doesn't."""
        if not self.client.bucket_exists(CONFIG.minio_bucket_name):
            # Create bucket if it doesn't exist
            self.client.make_bucket(CONFIG.minio_bucket_name)
            logger.info(f"Bucket {CONFIG.minio_bucket_name} created")

    def upload_file(self, file: UploadFile) -> bool:
        """Upload a file to Minio."""
        try:
            result = self.client.put_object(
                CONFIG.minio_bucket_name, file.filename, file.file, file.size
            )
        except Exception as e:
            logger.error(f"Error uploading file to Minio: {e}")
            return False
        logger.info(f"File uploaded to Minio: {result.object_name}")
        return True

    def get_file(self, filename: str) -> Optional[bytes]:
        """Get a file from Minio."""
        try:
            response = None
            try:
                response = self.client.get_object(CONFIG.minio_bucket_name, filename)
            finally:
                if response:
                    response.close()
                    response.release_conn()

            return response.data
        except Exception as e:
            logger.error(f"Error getting file from Minio: {e}")
            return None

    def delete_file(self, filename: str) -> bool:
        """Delete a file from Minio."""
        try:
            self.client.remove_object(CONFIG.minio_bucket_name, filename)
            return True
        except Exception as e:
            logger.error(f"Error deleting file from Minio: {e}")
            return False


MINIO_CLIENT = MinioClient()
