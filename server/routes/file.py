from fastapi import APIRouter, Depends, HTTPException, UploadFile

from models import File, FileUpload, User
from models.enums import FileType
from server import MINIO_CLIENT
from server.enums import FileUploadStatus
from server.utils import construct_filename, current_user

router = APIRouter(prefix="/file", tags=["file"])


@router.post("", response_model=str)
async def upload_file(input: FileUpload, user: User = Depends(current_user)):
    """Upload a file."""

    # overwrite the filename with the internal filename
    filename = construct_filename(input.filename, FileType.REPAIR_MANUAL, user.id)

    # minio client handles validation
    status = MINIO_CLIENT.upload_file(input)

    # handle status codes
    match status:
        case FileUploadStatus.FAILED_TOO_LARGE:
            raise HTTPException(
                status_code=413, detail="File is too large - exceeds 5MB"
            )
        case FileUploadStatus.FAILED_INVALID_FILE_TYPE:
            raise HTTPException(status_code=415, detail="File is not a valid file type")
        case FileUploadStatus.FAILED_UNKNOWN:
            raise HTTPException(status_code=500, detail="Unknown error")
        case FileUploadStatus.SUCCESS:
            pass

    return filename


@router.get("/{filename}", response_model=bytes)
async def get_file(filename: str, user: User = Depends(current_user)):
    """
    Get a file by its internal filename.
    Only the authorized user has access to the internal filename,
    so we can use it to check if the user is the owner of the file.
    """
    if user.id not in filename:
        raise HTTPException(status_code=403, detail="Unauthorized")

    file = MINIO_CLIENT.get_file(filename)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return file


@router.delete("/{filename}")
async def delete_file(filename: str):
    """Delete a file."""
    return MINIO_CLIENT.delete_file(filename)
