import shutil
from typing import List

from fastapi import Depends
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import status
from passlib.hash import pbkdf2_sha256
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound

from ..config import PROJECT_ROOT
from ..config import Settings
from ..config import get_settings
from ..database import Session
from ..database import get_session
from .models import Account
from .schemas import AccountCreate
from .schemas import AccountUpdate


class AccountService:
    def __init__(
        self,
        session: Session = Depends(get_session),
        settings: Settings = Depends(get_settings),
    ):
        self.session = session
        self.settings = settings

    def create_account(self, account_create: AccountCreate):
        account = Account(
            email=account_create.email,
            username=account_create.username,
            password=pbkdf2_sha256.hash(account_create.password),
        )
        self.session.add(account)
        try:
            self.session.commit()
            return account
        except IntegrityError:
            raise HTTPException(status.HTTP_409_CONFLICT) from None

    def get_accounts(self) -> List[Account]:
        accounts = self.session.execute(
            select(Account)
        ).scalars().all()
        return accounts

    def get_account(self, account_id: int) -> Account:
        return self._get_account(account_id)

    def update_account(self, account_id: int, account_update: AccountUpdate):
        account = self._get_account(account_id)

        if not account_update.first_name and not account_update.last_name:
            return

        account.first_name = account_update.first_name or account.first_name
        account.last_name = account_update.last_name or account.last_name

        self.session.commit()
        return account

    def update_account_avatar(self, account_id: int, avatar: UploadFile):
        account = self._get_account(account_id)

        filepath = PROJECT_ROOT / self.settings.static_directory / avatar.filename
        with filepath.open(mode='wb') as f:
            shutil.copyfileobj(avatar.file, f)
        file_url = f'{self.settings.static_url}/{avatar.filename}'

        account.avatar = file_url

        self.session.commit()
        return account

    def _get_account(self, account_id: int) -> Account:
        try:
            account = self.session.execute(
                select(Account)
                .where(Account.id == account_id)
            ).scalar_one()
            return account
        except NoResultFound:
            raise HTTPException(status.HTTP_404_NOT_FOUND) from None
