from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from ..database import Base


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    id = Column(Integer, primary_key=True)
    account_id = Column(ForeignKey('accounts.id'), nullable=False, unique=True)
    token = Column(String, nullable=False)
