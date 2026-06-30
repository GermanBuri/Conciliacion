import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_active_user, get_db
from app.models.user import User
from app.schemas.bank_transaction import BankTransactionListResponse, BankTransactionRead
from app.services.bank_transactions import BankTransactionService

router = APIRouter()


@router.get("/", response_model=BankTransactionListResponse)
def list_bank_transactions(
    batch_id: uuid.UUID | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> BankTransactionListResponse:
    return BankTransactionService(db).list_transactions(
        company_id=current_user.company_id,
        batch_id=batch_id,
        skip=skip,
        limit=limit,
    )


@router.get("/by-batch/{batch_id}", response_model=BankTransactionListResponse)
def list_bank_transactions_by_batch(
    batch_id: uuid.UUID,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> BankTransactionListResponse:
    return BankTransactionService(db).list_transactions(
        company_id=current_user.company_id,
        batch_id=batch_id,
        skip=skip,
        limit=limit,
    )


@router.get("/{transaction_id}", response_model=BankTransactionRead)
def get_bank_transaction(
    transaction_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> BankTransactionRead:
    transaction = BankTransactionService(db).get_transaction(
        transaction_id=transaction_id,
        company_id=current_user.company_id,
    )
    return BankTransactionRead.model_validate(transaction)
