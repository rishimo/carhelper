from asyncio import gather

from fastapi import APIRouter, Depends, HTTPException

from database.utils import (add_file_to_entity_by_id,
                            delete_file_from_entity_by_id)
from models import File, FileReturn, FileUpload, User
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

    # create File object
    file = File(
        type=input.file_type,
        title=input.title,
        internal_filename=filename,
        owner=user.id,
        description=input.description,
        entity_id=input.entity_id,
    )

    # associate the file with the corresponding entity
    add_file = add_file_to_entity_by_id(file.id, input.entity_id)

    await gather(add_file, file.save())

    return file.id


@router.get("/{file_id}", response_model=FileReturn)
async def get_file(file_id: str, user: User = Depends(current_user)):
    """
    Get a file by its ID.
    Only the authorized user has access to the internal filename,
    so we can use it to check if the user is the owner of the file.
    """
    # get the file metadata from the database
    file: File | None = await File.find_by_id(file_id)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")

    if not file.check_owner(user.id):
        raise HTTPException(status_code=403, detail="Unauthorized")

    data = MINIO_CLIENT.get_file(file.internal_filename)
    if data is None:
        raise HTTPException(status_code=404, detail="File not found")

    return FileReturn(data=data, **file.model_dump())


@router.delete("/{file_id}")
async def delete_file(file_id: str, user: User = Depends(current_user)):
    """Delete a file."""
    # get the file metadata from the database
    file: File | None = await File.find_by_id(file_id)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")

    if not file.check_owner(user.id):
        raise HTTPException(status_code=403, detail="Unauthorized")

    delete_file = file.delete()
    delete_file_from_entity = delete_file_from_entity_by_id(file.id, file.entity_id)

    await gather(delete_file, delete_file_from_entity)

    return MINIO_CLIENT.delete_file(file.internal_filename)
