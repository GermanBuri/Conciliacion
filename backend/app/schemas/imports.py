import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ImportBatchRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    company_id: uuid.UUID | None
    file_id: uuid.UUID
    batch_type: str
    status: str
    total_records: int
    valid_records: int
    invalid_records: int
    created_at: datetime


class ImportBatchListResponse(BaseModel):
    items: list[ImportBatchRead]
    total: int
