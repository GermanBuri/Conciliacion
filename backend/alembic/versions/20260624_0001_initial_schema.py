"""initial schema

Revision ID: 20260624_0001
Revises:
Create Date: 2026-06-24 09:20:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "20260624_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("legal_name", sa.String(length=255), nullable=False),
        sa.Column("tax_id", sa.String(length=50), nullable=False),
        sa.Column("base_currency", sa.String(length=10), nullable=False),
        sa.Column("timezone", sa.String(length=50), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_index(op.f("ix_companies_tax_id"), "companies", ["tax_id"], unique=False)

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_users_company_id"), "users", ["company_id"], unique=False)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=False)

    op.create_table(
        "uploaded_files",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("uploaded_by_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("file_type", sa.String(length=30), nullable=False),
        sa.Column("processing_status", sa.String(length=30), nullable=False),
        sa.Column("source_name", sa.String(length=255), nullable=False),
        sa.Column("stored_name", sa.String(length=255), nullable=False),
        sa.Column("storage_path", sa.Text(), nullable=False),
        sa.Column("mime_type", sa.String(length=100), nullable=True),
        sa.Column("extension", sa.String(length=10), nullable=False),
        sa.Column("size_bytes", sa.BigInteger(), nullable=False),
        sa.Column("checksum_sha256", sa.String(length=64), nullable=False),
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["uploaded_by_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("stored_name"),
    )
    op.create_index(op.f("ix_uploaded_files_checksum_sha256"), "uploaded_files", ["checksum_sha256"], unique=False)
    op.create_index(op.f("ix_uploaded_files_company_id"), "uploaded_files", ["company_id"], unique=False)
    op.create_index(op.f("ix_uploaded_files_extension"), "uploaded_files", ["extension"], unique=False)
    op.create_index(op.f("ix_uploaded_files_file_type"), "uploaded_files", ["file_type"], unique=False)
    op.create_index(op.f("ix_uploaded_files_processing_status"), "uploaded_files", ["processing_status"], unique=False)
    op.create_index(op.f("ix_uploaded_files_uploaded_by_id"), "uploaded_files", ["uploaded_by_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_uploaded_files_uploaded_by_id"), table_name="uploaded_files")
    op.drop_index(op.f("ix_uploaded_files_processing_status"), table_name="uploaded_files")
    op.drop_index(op.f("ix_uploaded_files_file_type"), table_name="uploaded_files")
    op.drop_index(op.f("ix_uploaded_files_extension"), table_name="uploaded_files")
    op.drop_index(op.f("ix_uploaded_files_company_id"), table_name="uploaded_files")
    op.drop_index(op.f("ix_uploaded_files_checksum_sha256"), table_name="uploaded_files")
    op.drop_table("uploaded_files")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_index(op.f("ix_users_company_id"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_companies_tax_id"), table_name="companies")
    op.drop_table("companies")
