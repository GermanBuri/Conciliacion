"""add reconciliation audit logs

Revision ID: 20260630_0004
Revises: 20260626_0003
Create Date: 2026-06-30 13:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "20260630_0004"
down_revision = "20260626_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "reconciliation_audit_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("run_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("action", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["run_id"], ["reconciliation_runs.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_reconciliation_audit_logs_action"),
        "reconciliation_audit_logs",
        ["action"],
        unique=False,
    )
    op.create_index(
        op.f("ix_reconciliation_audit_logs_run_id"),
        "reconciliation_audit_logs",
        ["run_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_reconciliation_audit_logs_user_id"),
        "reconciliation_audit_logs",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_reconciliation_audit_logs_user_id"), table_name="reconciliation_audit_logs")
    op.drop_index(op.f("ix_reconciliation_audit_logs_run_id"), table_name="reconciliation_audit_logs")
    op.drop_index(op.f("ix_reconciliation_audit_logs_action"), table_name="reconciliation_audit_logs")
    op.drop_table("reconciliation_audit_logs")
