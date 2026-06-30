import uuid
from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.bank_transaction import BankTransaction
from app.models.import_batch import ImportBatch


class BankTransactionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def bulk_create(self, items: Sequence[BankTransaction]) -> None:
        self.db.add_all(list(items))
        self.db.commit()

    def get_by_id(
        self,
        transaction_id: uuid.UUID,
        *,
        company_id: uuid.UUID | None,
    ) -> BankTransaction | None:
        query = (
            select(BankTransaction)
            .join(ImportBatch, ImportBatch.id == BankTransaction.batch_id)
            .where(BankTransaction.id == transaction_id)
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
    ) -> tuple[Sequence[BankTransaction], int]:
        query = (
            select(BankTransaction)
            .join(ImportBatch, ImportBatch.id == BankTransaction.batch_id)
            .order_by(BankTransaction.transaction_date.desc(), BankTransaction.id.desc())
        )
        count_query = (
            select(func.count(BankTransaction.id))
            .select_from(BankTransaction)
            .join(ImportBatch, ImportBatch.id == BankTransaction.batch_id)
        )

        if company_id is not None:
            query = query.where(ImportBatch.company_id == company_id)
            count_query = count_query.where(ImportBatch.company_id == company_id)
        if batch_id is not None:
            query = query.where(BankTransaction.batch_id == batch_id)
            count_query = count_query.where(BankTransaction.batch_id == batch_id)

        items = self.db.execute(query.offset(skip).limit(limit)).scalars().all()
        total = self.db.execute(count_query).scalar_one()
        return items, total
