import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UploadedFileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    company_id: uuid.UUID | None
    uploaded_by_id: uuid.UUID
    file_type: str
    processing_status: str
    source_name: str
    stored_name: str
    storage_path: str
    mime_type: str | None
    extension: str
    size_bytes: int
    checksum_sha256: str
    metadata_json: dict | None
    created_at: datetime
    updated_at: datetime


class UploadedFileListResponse(BaseModel):
    items: list[UploadedFileRead]
    total: int
