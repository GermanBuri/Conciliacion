import uuid
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class BankTransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    batch_id: uuid.UUID
    transaction_date: date
    description: str
    reference: str | None
    amount: Decimal
    balance: Decimal | None
    document_number: str | None
    raw_data: dict


class BankTransactionListResponse(BaseModel):
    items: list[BankTransactionRead]
    total: int
