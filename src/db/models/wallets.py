# import logging
# logging.getLogger(__name__).info(f'importing module { __name__}')


from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, BigInteger

from db.core.base_model import Base, DefaultCols



class Wallets(Base):
    __tablename__ = 'wallets'

    id: Mapped[DefaultCols.intpk]
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.user_id'))
    name: Mapped[str]
    network: Mapped[str]
    address: Mapped[str]
    has_notifications: Mapped[bool] = mapped_column(default=True)

    user: Mapped['Users'] = relationship(back_populates='wallets')
    groups: Mapped[list['Groups']] = relationship(
        secondary='group_wallets', 
        back_populates='wallets'
    )
    
        