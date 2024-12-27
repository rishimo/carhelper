from fastapi import APIRouter, HTTPException, UploadFile

from models import File
from server.file import MINIO_CLIENT
from server.utils import hash_password

router = APIRouter(prefix="/file", tags=["file"])


@router.post("", response_model=File)
async def upload_file(input: UploadFile):
    """Upload a file."""
