import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin


class ReconciliationMatch(TimestampMixin, Base):
    __tablename__ = "reconciliation_matches"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("reconciliation_runs.id"), nullable=False, index=True
    )
    bank_transaction_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("bank_transactions.id"), nullable=True, index=True
    )
    ledger_transaction_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("ledger_transactions.id"), nullable=True, index=True
    )
    status: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    match_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    amount_difference: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    days_difference: Mapped[int | None] = mapped_column(Integer, nullable=True)
    description_similarity: Mapped[Decimal | None] = mapped_column(Numeric(5, 4), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
