import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.bank_transaction import BankTransactionRepository
from app.schemas.bank_transaction import BankTransactionListResponse


class BankTransactionService:
    def __init__(self, db: Session) -> None:
        self.repository = BankTransactionRepository(db)

    def list_transactions(
        self,
        *,
        company_id: uuid.UUID | None,
        batch_id: uuid.UUID | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> BankTransactionListResponse:
        items, total = self.repository.list_transactions(
            company_id=company_id,
            batch_id=batch_id,
            skip=skip,
            limit=limit,
        )
        return BankTransactionListResponse(items=items, total=total)

    def get_transaction(self, *, transaction_id: uuid.UUID, company_id: uuid.UUID | None):
        transaction = self.repository.get_by_id(transaction_id, company_id=company_id)
        if transaction is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movimiento bancario no encontrado.",
            )
        return transaction
