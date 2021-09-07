from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile
from fastapi import Form
from fastapi import Response

from .schemas import Account as AccountSchema
from .schemas import AccountCreate
from .schemas import AccountUpdate
from .services import AccountService


router = APIRouter()


def initialize_app(app: FastAPI):
    app.include_router(router)


@router.post('/create-account')
def create_account(
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    service: AccountService = Depends(),
):
    service.create_account(AccountCreate(
        email=email,
        username=username,
        password=password,
    ))
    return Response()


@router.get('/get-accounts', response_model=List[AccountSchema])
def get_accounts(
    service: AccountService = Depends(),
):
    return service.get_accounts()


@router.get('/get-account/{account_id}', response_model=AccountSchema)
def get_account(
    account_id: int,
    service: AccountService = Depends(),
):
    return service.get_account(account_id)


@router.patch('/edit-account/{account_id}')
def edit_account(
    account_id: int,
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    avatar: Optional[UploadFile] = File(None),
    service: AccountService = Depends(),
):
    service.update_account(
        account_id,
        AccountUpdate(
            first_name=first_name,
            last_name=last_name,
            avatar=avatar,
        ),
    )
    return Response()
