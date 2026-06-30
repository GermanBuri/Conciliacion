import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ReconciliationRunRequest(BaseModel):
    bank_batch_id: uuid.UUID
    ledger_batch_id: uuid.UUID
    tolerance_amount: Decimal = Field(default=Decimal("0.00"), ge=0)
    tolerance_days: int = Field(default=0, ge=0)


class ReconciliationManualMatchRequest(BaseModel):
    bank_transaction_id: uuid.UUID
    ledger_transaction_id: uuid.UUID
    notes: str | None = None


class ReconciliationUnmatchRequest(BaseModel):
    match_id: uuid.UUID
    notes: str | None = None


class ReconciliationAuditLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    run_id: uuid.UUID
    user_id: uuid.UUID | None
    action: str
    description: str
    metadata_json: dict | None
    created_at: datetime


class ReconciliationAuditLogListResponse(BaseModel):
    items: list[ReconciliationAuditLogRead]
    total: int


class ReconciliationMatchRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    run_id: uuid.UUID
    bank_transaction_id: uuid.UUID | None
    ledger_transaction_id: uuid.UUID | None
    status: str
    match_score: int
    amount_difference: Decimal | None
    days_difference: int | None
    description_similarity: Decimal | None
    notes: str | None
    created_at: datetime
    updated_at: datetime


class ReconciliationRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    company_id: uuid.UUID | None
    bank_batch_id: uuid.UUID
    ledger_batch_id: uuid.UUID
    created_by_id: uuid.UUID
    tolerance_amount: Decimal
    tolerance_days: int
    status: str
    total_bank: int
    total_ledger: int
    matched_count: int
    unmatched_bank_count: int
    unmatched_ledger_count: int
    possible_match_count: int
    created_at: datetime


class ReconciliationRunListResponse(BaseModel):
    items: list[ReconciliationRunRead]
    total: int


class ReconciliationRunDetail(ReconciliationRunRead):
    matches: list[ReconciliationMatchRead]
