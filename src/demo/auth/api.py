from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm

from .schemas import Token
from .services import AuthService
from ..exceptions import EntityDoesNotExistError


router = APIRouter(
    prefix='/auth',
)


@router.post('/login', response_model=Token)
def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(),
):
    try:
        return auth_service.authenticate(credentials.username, credentials.password)
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)


@router.post('/token')
def token(
    refresh_token: str = Form(...),
    auth_service: AuthService = Depends(),
):
    try:
        return auth_service.refresh_token_pair(refresh_token)
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
