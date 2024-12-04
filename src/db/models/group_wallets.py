from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, BigInteger, ForeignKeyConstraint

from db.core.base_model import Base


class GroupWallets(Base):
    __tablename__ = 'group_wallets'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    group_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ['user_id', 'group_id'],
            ['groups.user_id', 'groups.group_id']
        ),
    )