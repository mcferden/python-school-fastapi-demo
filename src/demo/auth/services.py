from datetime import datetime
from datetime import timedelta

from fastapi import Depends
from jose import jwt
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from .models import RefreshToken
from .schemas import Token
from ..accounts.models import Account
from ..config import Settings
from ..config import get_settings
from ..database import Session
from ..database import get_session
from ..exceptions import EntityDoesNotExistError


class AuthService:
    def __init__(
        self,
        session: Session = Depends(get_session),
        settings: Settings = Depends(get_settings),
    ):
        self.session = session
        self.settings = settings

    def authenticate(self, username: str, password: str) -> Token:
        try:
            account = self.session.execute(
                select(Account)
                .where(Account.username == username)
            ).scalar_one()
        except NoResultFound:
            raise EntityDoesNotExistError from None

        if not pbkdf2_sha256.verify(password, account.password):
            raise EntityDoesNotExistError

        return self.create_token_pair(account)

    def refresh_token_pair(self, refresh_token: str) -> Token:
        try:
            account = self.session.execute(
                select(Account)
                .join_from(Account, RefreshToken)
                .where(RefreshToken.token == refresh_token)
            ).scalar_one()
        except NoResultFound:
            raise EntityDoesNotExistError from None

        return self.create_token_pair(account)

    def create_token_pair(self, account: Account) -> Token:
        access_token = self.create_token(
            account,
            secret_key=self.settings.secret_key,
            lifetime=self.settings.jwt_access_lifetime,
        )
        refresh_token = self.create_token(
            account,
            secret_key=self.settings.secret_key,
            lifetime=self.settings.jwt_refresh_lifetime,
        )

        try:
            account_token = self.session.execute(
                select(RefreshToken)
                .where(RefreshToken.account_id == account.id)
            ).scalar_one()
            account_token.token = refresh_token
        except NoResultFound:
            account_token = RefreshToken(
                account_id=account.id,
                token=refresh_token,
            )
            self.session.add(account_token)

        self.session.commit()

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    @classmethod
    def create_token(cls, account: Account, *, secret_key: str, lifetime: int) -> str:
        now = datetime.utcnow()
        return jwt.encode({
            'sub': str(account.id),
            'exp': now + timedelta(seconds=lifetime),
            'iat': now,
            'nbf': now,
            'account': {
                'id': account.id,
                'email': account.email,
                'username': account.username,
            },
        }, secret_key, 'HS256')
