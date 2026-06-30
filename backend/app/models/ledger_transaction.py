import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class LedgerTransaction(Base):
    __tablename__ = "ledger_transactions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    batch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("import_batches.id"), nullable=False, index=True
    )
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    account_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    account_name: Mapped[str] = mapped_column(String(255), nullable=False)
    third_party: Mapped[str | None] = mapped_column(String(255), nullable=True)
    document_number: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    debit: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    credit: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    raw_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
