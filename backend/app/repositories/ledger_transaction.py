import uuid
from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.import_batch import ImportBatch
from app.models.ledger_transaction import LedgerTransaction


class LedgerTransactionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def bulk_create(self, items: Sequence[LedgerTransaction]) -> None:
        self.db.add_all(list(items))
        self.db.commit()

    def get_by_id(
        self,
        transaction_id: uuid.UUID,
        *,
        company_id: uuid.UUID | None,
    ) -> LedgerTransaction | None:
        query = (
            select(LedgerTransaction)
            .join(ImportBatch, ImportBatch.id == LedgerTransaction.batch_id)
            .where(LedgerTransaction.id == transaction_id)
        )
        if company_id is not None:
            query = query.where(ImportBatch.company_id == company_id)
        return self.db.execute(query).scalar_one_or_none()

    def list_transactions(
        self,
        *,
        company_id: uuid.UUID | None,
        batch_id: uuid.UUID | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> tuple[Sequence[LedgerTransaction], int]:
        query = (
            select(LedgerTransaction)
            .join(ImportBatch, ImportBatch.id == LedgerTransaction.batch_id)
            .order_by(LedgerTransaction.transaction_date.desc(), LedgerTransaction.id.desc())
        )
        count_query = (
            select(func.count(LedgerTransaction.id))
            .select_from(LedgerTransaction)
            .join(ImportBatch, ImportBatch.id == LedgerTransaction.batch_id)
        )

        if company_id is not None:
            query = query.where(ImportBatch.company_id == company_id)
            count_query = count_query.where(ImportBatch.company_id == company_id)
        if batch_id is not None:
            query = query.where(LedgerTransaction.batch_id == batch_id)
            count_query = count_query.where(LedgerTransaction.batch_id == batch_id)

        items = self.db.execute(query.offset(skip).limit(limit)).scalars().all()
        total = self.db.execute(count_query).scalar_one()
        return items, total
