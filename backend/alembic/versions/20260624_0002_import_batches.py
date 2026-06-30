"""add import batches and transactions

Revision ID: 20260624_0002
Revises: 20260624_0001
Create Date: 2026-06-24 11:30:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "20260624_0002"
down_revision = "20260624_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "import_batches",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("file_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("batch_type", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("total_records", sa.Integer(), nullable=False),
        sa.Column("valid_records", sa.Integer(), nullable=False),
        sa.Column("invalid_records", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["file_id"], ["uploaded_files.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_import_batches_batch_type"), "import_batches", ["batch_type"], unique=False)
    op.create_index(op.f("ix_import_batches_company_id"), "import_batches", ["company_id"], unique=False)
    op.create_index(op.f("ix_import_batches_file_id"), "import_batches", ["file_id"], unique=False)
    op.create_index(op.f("ix_import_batches_status"), "import_batches", ["status"], unique=False)

    op.create_table(
        "bank_transactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("batch_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("transaction_date", sa.Date(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("reference", sa.String(length=255), nullable=True),
        sa.Column("amount", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("balance", sa.Numeric(precision=18, scale=2), nullable=True),
        sa.Column("document_number", sa.String(length=100), nullable=True),
        sa.Column("raw_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(["batch_id"], ["import_batches.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_bank_transactions_batch_id"), "bank_transactions", ["batch_id"], unique=False)
    op.create_index(
        op.f("ix_bank_transactions_document_number"), "bank_transactions", ["document_number"], unique=False
    )
    op.create_index(
        op.f("ix_bank_transactions_transaction_date"), "bank_transactions", ["transaction_date"], unique=False
    )

    op.create_table(
        "ledger_transactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("batch_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("transaction_date", sa.Date(), nullable=False),
        sa.Column("account_code", sa.String(length=100), nullable=False),
        sa.Column("account_name", sa.String(length=255), nullable=False),
        sa.Column("third_party", sa.String(length=255), nullable=True),
        sa.Column("document_number", sa.String(length=100), nullable=True),
        sa.Column("debit", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("credit", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("raw_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(["batch_id"], ["import_batches.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ledger_transactions_account_code"), "ledger_transactions", ["account_code"], unique=False)
    op.create_index(op.f("ix_ledger_transactions_batch_id"), "ledger_transactions", ["batch_id"], unique=False)
    op.create_index(
        op.f("ix_ledger_transactions_document_number"), "ledger_transactions", ["document_number"], unique=False
    )
    op.create_index(
        op.f("ix_ledger_transactions_transaction_date"), "ledger_transactions", ["transaction_date"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_ledger_transactions_transaction_date"), table_name="ledger_transactions")
    op.drop_index(op.f("ix_ledger_transactions_document_number"), table_name="ledger_transactions")
    op.drop_index(op.f("ix_ledger_transactions_batch_id"), table_name="ledger_transactions")
    op.drop_index(op.f("ix_ledger_transactions_account_code"), table_name="ledger_transactions")
    op.drop_table("ledger_transactions")
    op.drop_index(op.f("ix_bank_transactions_transaction_date"), table_name="bank_transactions")
    op.drop_index(op.f("ix_bank_transactions_document_number"), table_name="bank_transactions")
    op.drop_index(op.f("ix_bank_transactions_batch_id"), table_name="bank_transactions")
    op.drop_table("bank_transactions")
    op.drop_index(op.f("ix_import_batches_status"), table_name="import_batches")
    op.drop_index(op.f("ix_import_batches_file_id"), table_name="import_batches")
    op.drop_index(op.f("ix_import_batches_company_id"), table_name="import_batches")
    op.drop_index(op.f("ix_import_batches_batch_type"), table_name="import_batches")
    op.drop_table("import_batches")
