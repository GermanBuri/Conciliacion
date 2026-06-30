import uuid
from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.uploaded_file import UploadedFile


class UploadedFileRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, file_id: uuid.UUID, *, company_id: uuid.UUID | None = None) -> UploadedFile | None:
        query = select(UploadedFile).where(UploadedFile.id == file_id)
        if company_id is not None:
            query = query.where(UploadedFile.company_id == company_id)
        return self.db.execute(query).scalar_one_or_none()

    def create(
        self,
        *,
        company_id,
        uploaded_by_id,
        file_type: str,
        processing_status: str,
        source_name: str,
        stored_name: str,
        storage_path: str,
        mime_type: str | None,
        extension: str,
        size_bytes: int,
        checksum_sha256: str,
        metadata_json: dict | None = None,
    ) -> UploadedFile:
        uploaded_file = UploadedFile(
            company_id=company_id,
            uploaded_by_id=uploaded_by_id,
            file_type=file_type,
            processing_status=processing_status,
            source_name=source_name,
            stored_name=stored_name,
            storage_path=storage_path,
            mime_type=mime_type,
            extension=extension,
            size_bytes=size_bytes,
            checksum_sha256=checksum_sha256,
            metadata_json=metadata_json,
        )
        self.db.add(uploaded_file)
        self.db.commit()
        self.db.refresh(uploaded_file)
        return uploaded_file

    def list_files(
        self,
        *,
        file_type: str | None = None,
        company_id=None,
        skip: int = 0,
        limit: int = 50,
    ) -> tuple[Sequence[UploadedFile], int]:
        filters = []
        if file_type:
            filters.append(UploadedFile.file_type == file_type)
        if company_id:
            filters.append(UploadedFile.company_id == company_id)

        query = select(UploadedFile).order_by(UploadedFile.created_at.desc())
        count_query = select(func.count(UploadedFile.id))

        for condition in filters:
            query = query.where(condition)
            count_query = count_query.where(condition)

        items = self.db.execute(query.offset(skip).limit(limit)).scalars().all()
        total = self.db.execute(count_query).scalar_one()
        return items, total

    def update_processing_status(self, uploaded_file: UploadedFile, *, processing_status: str) -> UploadedFile:
        uploaded_file.processing_status = processing_status
        self.db.add(uploaded_file)
        self.db.commit()
        self.db.refresh(uploaded_file)
        return uploaded_file
