from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger

from db.core.base_model import Base, DefaultCols


class Users(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str]
    first_name: Mapped[str]
    reg_time: Mapped[datetime]

    wallets: Mapped[list['Wallets']] = relationship(back_populates='user')
    groups: Mapped[list['Groups']] = relationship(back_populates='user')
        