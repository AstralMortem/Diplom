from fastapi import APIRouter, UploadFile, File, Depends
from backend.services.files import get_file_service, FileService, FileResponse
from backend.utils.permission_helper import HasPermission

file_router = APIRouter(prefix="/files", tags=["files"])


@file_router.post("/upload", response_model=FileResponse, dependencies=[Depends(HasPermission("upload", "files"), )])
async def upload_file(file_path: str, file_name: str,file: UploadFile = File(...), service: FileService = Depends(get_file_service)):
    print(file_path, file_name, file)
    return await service.upload_file(file_path, file_name, file)
