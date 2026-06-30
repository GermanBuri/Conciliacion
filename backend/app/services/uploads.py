import hashlib
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.repositories.uploaded_file import UploadedFileRepository
from app.schemas.upload import UploadedFileListResponse

ALLOWED_EXTENSIONS = {".xlsx", ".xls", ".csv", ".txt"}
FILE_TYPE_DIRECTORIES = {
    "bank_statement": "bank",
    "ledger": "ledger",
}
INITIAL_PROCESSING_STATUS = "uploaded"


class UploadService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = UploadedFileRepository(db)

    async def save_uploaded_file(
        self,
        *,
        upload: UploadFile,
        file_type: str,
        current_user: User,
        company_id=None,
    ):
        self._validate_file_type(file_type)
        source_name = Path(upload.filename or "").name
        if not source_name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo debe incluir un nombre valido.",
            )
        extension = Path(source_name).suffix.lower()
        self._validate_extension(extension)

        content = await upload.read()
        await upload.close()
        self._validate_size(len(content))
        if len(content) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo no puede estar vacio.",
            )

        checksum = hashlib.sha256(content).hexdigest()
        stored_name = f"{uuid.uuid4().hex}{extension}"
        storage_dir = settings.upload_path / FILE_TYPE_DIRECTORIES[file_type]
        storage_dir.mkdir(parents=True, exist_ok=True)
        file_path = (storage_dir / stored_name).resolve()
        self._validate_storage_path(file_path)
        file_path.write_bytes(content)

        return self.repository.create(
            company_id=company_id or current_user.company_id,
            uploaded_by_id=current_user.id,
            file_type=file_type,
            processing_status=INITIAL_PROCESSING_STATUS,
            source_name=source_name,
            stored_name=stored_name,
            storage_path=str(file_path),
            mime_type=upload.content_type,
            extension=extension,
            size_bytes=len(content),
            checksum_sha256=checksum,
            metadata_json={"original_filename": source_name},
        )

    def list_uploaded_files(
        self,
        *,
        file_type: str | None = None,
        company_id=None,
        skip: int = 0,
        limit: int = 50,
    ) -> UploadedFileListResponse:
        if file_type is not None:
            self._validate_file_type(file_type)
        items, total = self.repository.list_files(
            file_type=file_type,
            company_id=company_id,
            skip=skip,
            limit=limit,
        )
        return UploadedFileListResponse(items=items, total=total)

    @staticmethod
    def _validate_file_type(file_type: str) -> None:
        if file_type not in FILE_TYPE_DIRECTORIES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo de archivo no soportado.",
            )

    @staticmethod
    def _validate_extension(extension: str) -> None:
        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Extension no permitida. Use Excel, CSV o TXT.",
            )

    @staticmethod
    def _validate_size(size_bytes: int) -> None:
        max_size_bytes = settings.max_upload_size_mb * 1024 * 1024
        if size_bytes > max_size_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"El archivo supera el maximo permitido de {settings.max_upload_size_mb} MB.",
            )

    @staticmethod
    def _validate_storage_path(file_path: Path) -> None:
        upload_root = settings.upload_path.resolve()
        if upload_root not in file_path.parents:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No fue posible determinar una ruta segura de almacenamiento.",
            )
