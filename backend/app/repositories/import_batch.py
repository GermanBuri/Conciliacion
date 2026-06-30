import uuid
from collections.abc import Sequence

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.models.import_batch import ImportBatch


class ImportBatchRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        company_id: uuid.UUID | None,
        file_id: uuid.UUID,
        batch_type: str,
        status: str,
    ) -> ImportBatch:
        import_batch = ImportBatch(
            company_id=company_id,
            file_id=file_id,
            batch_type=batch_type,
            status=status,
            total_records=0,
            valid_records=0,
            invalid_records=0,
        )
        self.db.add(import_batch)
        self.db.commit()
        self.db.refresh(import_batch)
        return import_batch

    def update_counts_and_status(
        self,
        import_batch: ImportBatch,
        *,
        status: str,
        total_records: int,
        valid_records: int,
        invalid_records: int,
    ) -> ImportBatch:
        import_batch.status = status
        import_batch.total_records = total_records
        import_batch.valid_records = valid_records
        import_batch.invalid_records = invalid_records
        self.db.add(import_batch)
        self.db.commit()
        self.db.refresh(import_batch)
        return import_batch

    def update_status(self, import_batch: ImportBatch, *, status: str) -> ImportBatch:
        import_batch.status = status
        self.db.add(import_batch)
        self.db.commit()
        self.db.refresh(import_batch)
        return import_batch

    def get_by_id(self, batch_id: uuid.UUID, *, company_id: uuid.UUID | None) -> ImportBatch | None:
        query = select(ImportBatch).where(ImportBatch.id == batch_id)
        if company_id is not None:
            query = query.where(ImportBatch.company_id == company_id)
        return self.db.execute(query).scalar_one_or_none()

    def get_latest_by_file_id(self, file_id: uuid.UUID) -> ImportBatch | None:
        query = (
            select(ImportBatch)
            .where(ImportBatch.file_id == file_id)
            .order_by(desc(ImportBatch.created_at))
            .limit(1)
        )
        return self.db.execute(query).scalar_one_or_none()

    def list_batches(
        self,
        *,
        company_id: uuid.UUID | None,
        skip: int = 0,
        limit: int = 50,
    ) -> tuple[Sequence[ImportBatch], int]:
        query = select(ImportBatch).order_by(ImportBatch.created_at.desc())
        count_query = select(func.count(ImportBatch.id))
        if company_id is not None:
            query = query.where(ImportBatch.company_id == company_id)
            count_query = count_query.where(ImportBatch.company_id == company_id)

        items = self.db.execute(query.offset(skip).limit(limit)).scalars().all()
        total = self.db.execute(count_query).scalar_one()
        return items, total
