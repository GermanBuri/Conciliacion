import uuid
from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.reconciliation_audit_log import ReconciliationAuditLog
from app.models.reconciliation_match import ReconciliationMatch
from app.models.reconciliation_run import ReconciliationRun


class ReconciliationRunRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, run: ReconciliationRun) -> ReconciliationRun:
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)
        return run

    def save(self, run: ReconciliationRun) -> ReconciliationRun:
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)
        return run

    def get_by_id(self, run_id: uuid.UUID, *, company_id: uuid.UUID | None) -> ReconciliationRun | None:
        query = select(ReconciliationRun).where(ReconciliationRun.id == run_id)
        if company_id is not None:
            query = query.where(ReconciliationRun.company_id == company_id)
        return self.db.execute(query).scalar_one_or_none()

    def list_runs(
        self,
        *,
        company_id: uuid.UUID | None,
        skip: int = 0,
        limit: int = 50,
    ) -> tuple[Sequence[ReconciliationRun], int]:
        query = select(ReconciliationRun).order_by(ReconciliationRun.created_at.desc())
        count_query = select(func.count(ReconciliationRun.id))
        if company_id is not None:
            query = query.where(ReconciliationRun.company_id == company_id)
            count_query = count_query.where(ReconciliationRun.company_id == company_id)

        items = self.db.execute(query.offset(skip).limit(limit)).scalars().all()
        total = self.db.execute(count_query).scalar_one()
        return items, total


class ReconciliationMatchRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def bulk_create(self, matches: Sequence[ReconciliationMatch]) -> None:
        self.db.add_all(list(matches))
        self.db.commit()

    def create(self, match: ReconciliationMatch) -> ReconciliationMatch:
        self.db.add(match)
        self.db.commit()
        self.db.refresh(match)
        return match

    def list_by_run_id(self, run_id: uuid.UUID) -> Sequence[ReconciliationMatch]:
        query = (
            select(ReconciliationMatch)
            .where(ReconciliationMatch.run_id == run_id)
            .order_by(ReconciliationMatch.status.asc(), ReconciliationMatch.created_at.asc())
        )
        return self.db.execute(query).scalars().all()

    def get_by_id(self, match_id: uuid.UUID, *, run_id: uuid.UUID) -> ReconciliationMatch | None:
        query = select(ReconciliationMatch).where(
            ReconciliationMatch.id == match_id,
            ReconciliationMatch.run_id == run_id,
        )
        return self.db.execute(query).scalar_one_or_none()

    def delete(self, match: ReconciliationMatch) -> None:
        self.db.delete(match)
        self.db.commit()

    def delete_many(self, matches: Sequence[ReconciliationMatch]) -> None:
        for match in matches:
            self.db.delete(match)
        self.db.commit()


class ReconciliationAuditLogRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, audit_log: ReconciliationAuditLog) -> ReconciliationAuditLog:
        self.db.add(audit_log)
        self.db.commit()
        self.db.refresh(audit_log)
        return audit_log

    def list_by_run_id(self, run_id: uuid.UUID) -> tuple[Sequence[ReconciliationAuditLog], int]:
        query = (
            select(ReconciliationAuditLog)
            .where(ReconciliationAuditLog.run_id == run_id)
            .order_by(ReconciliationAuditLog.created_at.desc(), ReconciliationAuditLog.id.desc())
        )
        count_query = (
            select(func.count(ReconciliationAuditLog.id))
            .select_from(ReconciliationAuditLog)
            .where(ReconciliationAuditLog.run_id == run_id)
        )
        items = self.db.execute(query).scalars().all()
        total = self.db.execute(count_query).scalar_one()
        return items, total
