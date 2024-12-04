from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, BigInteger

from db.core.base_model import Base, DefaultCols



class Groups(Base):
    __tablename__ = 'groups'

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.user_id'), primary_key=True)
    group_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str]

    user: Mapped['Users'] = relationship(back_populates='groups')
    wallets: Mapped[list['Wallets']] = relationship(
        secondary='group_wallets', 
        back_populates='groups'
    )
    
        