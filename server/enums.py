from enum import Enum


class FileUploadStatus(str, Enum):
    """File upload status enum."""

    SUCCESS = "SUCCESS"
    FAILED_TOO_LARGE = "FAILED_TOO_LARGE"
    FAILED_INVALID_FILE_TYPE = "FAILED_INVALID_FILE_TYPE"
    FAILED_UNKNOWN = "FAILED_UNKNOWN"
