from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_active_user, get_db
from app.models.user import User
from app.schemas.upload import UploadedFileListResponse, UploadedFileRead
from app.services.uploads import UploadService

router = APIRouter()


@router.post("/bank-statements", response_model=UploadedFileRead, status_code=201)
@router.post("/bank-files", response_model=UploadedFileRead, status_code=201)
async def upload_bank_statement(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> UploadedFileRead:
    uploaded_file = await UploadService(db).save_uploaded_file(
        upload=file,
        file_type="bank_statement",
        current_user=current_user,
    )
    return UploadedFileRead.model_validate(uploaded_file)


@router.post("/ledger-files", response_model=UploadedFileRead, status_code=201)
async def upload_ledger_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> UploadedFileRead:
    uploaded_file = await UploadService(db).save_uploaded_file(
        upload=file,
        file_type="ledger",
        current_user=current_user,
    )
    return UploadedFileRead.model_validate(uploaded_file)


@router.get("/", response_model=UploadedFileListResponse)
def list_uploaded_files(
    file_type: str | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> UploadedFileListResponse:
    return UploadService(db).list_uploaded_files(
        file_type=file_type,
        company_id=current_user.company_id,
        skip=skip,
        limit=limit,
    )
