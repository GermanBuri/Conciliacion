import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from starlette.background import BackgroundTask

from app.api.v1.deps import get_current_active_user, get_db
from app.models.user import User
from app.schemas.reconciliation import (
    ReconciliationAuditLogListResponse,
    ReconciliationManualMatchRequest,
    ReconciliationRunDetail,
    ReconciliationRunListResponse,
    ReconciliationRunRequest,
    ReconciliationUnmatchRequest,
)
from app.services.reconciliations import ReconciliationService

router = APIRouter()


@router.post("/run", response_model=ReconciliationRunDetail, status_code=status.HTTP_201_CREATED)
def run_reconciliation(
    payload: ReconciliationRunRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ReconciliationRunDetail:
    return ReconciliationService(db).run(payload=payload, current_user=current_user)


@router.get("/", response_model=ReconciliationRunListResponse)
def list_reconciliations(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ReconciliationRunListResponse:
    return ReconciliationService(db).list_runs(
        company_id=current_user.company_id,
        skip=skip,
        limit=limit,
    )


@router.get("/{id}", response_model=ReconciliationRunDetail)
def get_reconciliation(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ReconciliationRunDetail:
    return ReconciliationService(db).get_run(run_id=id, company_id=current_user.company_id)


@router.get("/{run_id}/export")
def export_reconciliation(
    run_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> FileResponse:
    file_path, filename = ReconciliationService(db).export_run(
        run_id=run_id,
        company_id=current_user.company_id,
        user_id=current_user.id,
    )
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        background=BackgroundTask(Path(file_path).unlink, missing_ok=True),
    )


@router.post("/{run_id}/manual-match", response_model=ReconciliationRunDetail)
def manual_match_reconciliation(
    run_id: uuid.UUID,
    payload: ReconciliationManualMatchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ReconciliationRunDetail:
    return ReconciliationService(db).manual_match(
        run_id=run_id,
        payload=payload,
        company_id=current_user.company_id,
        user_id=current_user.id,
    )


@router.post("/{run_id}/unmatch", response_model=ReconciliationRunDetail)
def unmatch_reconciliation(
    run_id: uuid.UUID,
    payload: ReconciliationUnmatchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ReconciliationRunDetail:
    return ReconciliationService(db).unmatch(
        run_id=run_id,
        payload=payload,
        company_id=current_user.company_id,
        user_id=current_user.id,
    )


@router.get("/{run_id}/audit", response_model=ReconciliationAuditLogListResponse)
def get_reconciliation_audit(
    run_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ReconciliationAuditLogListResponse:
    return ReconciliationService(db).list_audit_logs(
        run_id=run_id,
        company_id=current_user.company_id,
    )
