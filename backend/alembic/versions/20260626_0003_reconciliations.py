"""add reconciliation runs and matches

Revision ID: 20260626_0003
Revises: 20260624_0002
Create Date: 2026-06-26 10:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "20260626_0003"
down_revision = "20260624_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "reconciliation_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("bank_batch_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("ledger_batch_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_by_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tolerance_amount", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("tolerance_days", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("total_bank", sa.Integer(), nullable=False),
        sa.Column("total_ledger", sa.Integer(), nullable=False),
        sa.Column("matched_count", sa.Integer(), nullable=False),
        sa.Column("unmatched_bank_count", sa.Integer(), nullable=False),
        sa.Column("unmatched_ledger_count", sa.Integer(), nullable=False),
        sa.Column("possible_match_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["bank_batch_id"], ["import_batches.id"]),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["ledger_batch_id"], ["import_batches.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_reconciliation_runs_bank_batch_id"), "reconciliation_runs", ["bank_batch_id"], unique=False)
    op.create_index(op.f("ix_reconciliation_runs_company_id"), "reconciliation_runs", ["company_id"], unique=False)
    op.create_index(op.f("ix_reconciliation_runs_created_by_id"), "reconciliation_runs", ["created_by_id"], unique=False)
    op.create_index(op.f("ix_reconciliation_runs_ledger_batch_id"), "reconciliation_runs", ["ledger_batch_id"], unique=False)
    op.create_index(op.f("ix_reconciliation_runs_status"), "reconciliation_runs", ["status"], unique=False)

    op.create_table(
        "reconciliation_matches",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("run_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("bank_transaction_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("ledger_transaction_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("match_score", sa.Integer(), nullable=False),
        sa.Column("amount_difference", sa.Numeric(precision=18, scale=2), nullable=True),
        sa.Column("days_difference", sa.Integer(), nullable=True),
        sa.Column("description_similarity", sa.Numeric(precision=5, scale=4), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["bank_transaction_id"], ["bank_transactions.id"]),
        sa.ForeignKeyConstraint(["ledger_transaction_id"], ["ledger_transactions.id"]),
        sa.ForeignKeyConstraint(["run_id"], ["reconciliation_runs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_reconciliation_matches_bank_transaction_id"),
        "reconciliation_matches",
        ["bank_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_reconciliation_matches_ledger_transaction_id"),
        "reconciliation_matches",
        ["ledger_transaction_id"],
        unique=False,
    )
    op.create_index(op.f("ix_reconciliation_matches_run_id"), "reconciliation_matches", ["run_id"], unique=False)
    op.create_index(op.f("ix_reconciliation_matches_status"), "reconciliation_matches", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_reconciliation_matches_status"), table_name="reconciliation_matches")
    op.drop_index(op.f("ix_reconciliation_matches_run_id"), table_name="reconciliation_matches")
    op.drop_index(op.f("ix_reconciliation_matches_ledger_transaction_id"), table_name="reconciliation_matches")
    op.drop_index(op.f("ix_reconciliation_matches_bank_transaction_id"), table_name="reconciliation_matches")
    op.drop_table("reconciliation_matches")
    op.drop_index(op.f("ix_reconciliation_runs_status"), table_name="reconciliation_runs")
    op.drop_index(op.f("ix_reconciliation_runs_ledger_batch_id"), table_name="reconciliation_runs")
    op.drop_index(op.f("ix_reconciliation_runs_created_by_id"), table_name="reconciliation_runs")
    op.drop_index(op.f("ix_reconciliation_runs_company_id"), table_name="reconciliation_runs")
    op.drop_index(op.f("ix_reconciliation_runs_bank_batch_id"), table_name="reconciliation_runs")
    op.drop_table("reconciliation_runs")
