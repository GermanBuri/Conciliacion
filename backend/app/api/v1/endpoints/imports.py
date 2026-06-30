import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_active_user, get_db
from app.models.user import User
from app.schemas.imports import ImportBatchListResponse, ImportBatchRead
from app.services.imports import ImportService

router = APIRouter()


@router.post("/process/{file_id}", response_model=ImportBatchRead, status_code=status.HTTP_201_CREATED)
def process_import_file(
    file_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ImportBatchRead:
    import_batch = ImportService(db).process_file(file_id=file_id, current_user=current_user)
    return ImportBatchRead.model_validate(import_batch)


@router.get("/", response_model=ImportBatchListResponse)
def list_import_batches(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ImportBatchListResponse:
    return ImportService(db).list_batches(
        company_id=current_user.company_id,
        skip=skip,
        limit=limit,
    )


@router.get("/{batch_id}", response_model=ImportBatchRead)
def get_import_batch(
    batch_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ImportBatchRead:
    import_batch = ImportService(db).get_batch(batch_id=batch_id, company_id=current_user.company_id)
    return ImportBatchRead.model_validate(import_batch)
