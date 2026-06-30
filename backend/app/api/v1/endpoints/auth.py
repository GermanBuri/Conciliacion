from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_active_user, get_db
from app.core.security import create_access_token
from app.schemas.auth import LoginResponse
from app.schemas.user import UserRead
from app.services.auth import AuthService

router = APIRouter()

INVALID_CREDENTIALS_MESSAGE = "Credenciales incorrectas."


@router.post("/login", response_model=LoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> LoginResponse:
    user = AuthService(db).authenticate_user(
        email=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_CREDENTIALS_MESSAGE,
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario esta inactivo.",
        )

    access_token = create_access_token(subject=user.email)
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserRead.model_validate(user),
    )


@router.get("/me", response_model=UserRead)
def read_current_user(current_user=Depends(get_current_active_user)) -> UserRead:
    return UserRead.model_validate(current_user)
