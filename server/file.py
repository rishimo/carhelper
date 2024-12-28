from logging import get_logger
from typing import Optional

import minio
from fastapi import UploadFile

from server import CONFIG
from server.enums import FileUploadStatus

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

    def _validate_file(self, file: UploadFile) -> FileUploadStatus:
        """Validate a file."""

        if file.size > 5 * 1024 * 1024:
            logger.error("File is too large - exceeds 5MB")
            return FileUploadStatus.FAILED_TOO_LARGE

        if file.content_type not in ["application/pdf", "image/jpeg", "image/png"]:
            logger.error("File is not a valid file type")
            return FileUploadStatus.FAILED_INVALID_FILE_TYPE

        return FileUploadStatus.SUCCESS

    async def upload_file(self, file: UploadFile) -> FileUploadStatus:
        """Upload a file to Minio."""
        valid = self._validate_file(file)

        if valid != FileUploadStatus.SUCCESS:
            return valid

        try:
            result = self.client.put_object(
                CONFIG.minio_bucket_name, file.filename, await file.read(), file.size
            )
        except Exception as e:
            logger.error(f"Error uploading file to Minio: {e}")
            return FileUploadStatus.FAILED_UNKNOWN

        logger.info(f"File uploaded to Minio: {result.object_name}")
        return FileUploadStatus.SUCCESS

    async def get_file(self, filename: str) -> Optional[bytes]:
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

    async def delete_file(self, filename: str) -> bool:
        """Delete a file from Minio."""
        try:
            self.client.remove_object(CONFIG.minio_bucket_name, filename)
            return True
        except Exception as e:
            logger.error(f"Error deleting file from Minio: {e}")
            return False


MINIO_CLIENT = MinioClient()
