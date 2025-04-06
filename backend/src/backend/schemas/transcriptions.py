import uuid
from .base import Schema


class TranscriptionCreate(Schema):
    record_id: uuid.UUID | None = None
    audio_url: str
    audio_duration: int = 0
    transcription_text: str

    asr_model: str = "whisper"
    asr_config: dict = {}
    language: str = "uk"


class TranscriptionRead(Schema):
    record_id: uuid.UUID
    transcription_id: int
    audio_url: str
    audio_duration: int
    transcription_text: str


class TranscriptionDetailRead(TranscriptionRead):
    asr_model: str
    asr_config: dict
    language: str
