import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_active_user, get_db
from app.models.user import User
from app.schemas.ledger_transaction import LedgerTransactionListResponse, LedgerTransactionRead
from app.services.ledger_transactions import LedgerTransactionService

router = APIRouter()


@router.get("/", response_model=LedgerTransactionListResponse)
def list_ledger_transactions(
    batch_id: uuid.UUID | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> LedgerTransactionListResponse:
    return LedgerTransactionService(db).list_transactions(
        company_id=current_user.company_id,
        batch_id=batch_id,
        skip=skip,
        limit=limit,
    )


@router.get("/by-batch/{batch_id}", response_model=LedgerTransactionListResponse)
def list_ledger_transactions_by_batch(
    batch_id: uuid.UUID,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> LedgerTransactionListResponse:
    return LedgerTransactionService(db).list_transactions(
        company_id=current_user.company_id,
        batch_id=batch_id,
        skip=skip,
        limit=limit,
    )


@router.get("/{transaction_id}", response_model=LedgerTransactionRead)
def get_ledger_transaction(
    transaction_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> LedgerTransactionRead:
    transaction = LedgerTransactionService(db).get_transaction(
        transaction_id=transaction_id,
        company_id=current_user.company_id,
    )
    return LedgerTransactionRead.model_validate(transaction)
