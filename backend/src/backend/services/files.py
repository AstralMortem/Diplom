from fastapi import UploadFile
from aiofiles import open
from backend.config import config
from backend.core import MedServiceException
from backend.schemas.base import Schema
import wave

def get_wav_duration(file_path):
    try:
        with wave.open(file_path, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = frames / float(rate)
            return int(duration)
    except Exception:
        return 0


class FileResponse(Schema):
    file_path: str
    file_name: str
    duration: int | None = None
    size: int



class FileService:

    async def upload_file(self,file_path: str, file_name: str, file: UploadFile):
        full_dir = config.MEDIA_DIR.joinpath(file_path)

        if not full_dir.exists():
            full_dir.mkdir(parents=True, exist_ok=True)

        full_path = full_dir.joinpath(file_name)
        
        try:
            async with open(full_path, "wb") as out_file:
                while content := await file.read(1024):
                    await out_file.write(content)

            if file_name.endswith(".wav"):
                duration = get_wav_duration(str(full_path))
            else:
                duration = None

            url = '/' + str(full_path.relative_to(config.MEDIA_DIR))
            url = '/media' + url.replace('\\', '/')

            return FileResponse(file_path=str(url), file_name=file_name, size=file.size, duration=duration)

        except Exception as e:
            print(e)
            raise MedServiceException(400, "Failed to upload file",f"Failed to upload file to {full_path}", debug=e)


async def get_file_service():
    return FileService()