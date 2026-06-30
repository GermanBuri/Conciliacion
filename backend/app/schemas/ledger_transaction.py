import uuid
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class LedgerTransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    batch_id: uuid.UUID
    transaction_date: date
    account_code: str
    account_name: str
    third_party: str | None
    document_number: str | None
    debit: Decimal
    credit: Decimal
    raw_data: dict


class LedgerTransactionListResponse(BaseModel):
    items: list[LedgerTransactionRead]
    total: int
