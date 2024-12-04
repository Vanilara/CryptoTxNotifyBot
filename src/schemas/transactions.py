from pydantic import BaseModel
from core.enums import TransferType
from schemas.wallets import BalanceDTO


class BaseTranfer(BaseModel):
    amount: float
    link: str
    network: str

class TransferDTO(BaseTranfer):
    addr_from: str
    addr_to: str

    @property
    def addresses(self) -> list[str]:
        return [self.addr_from, self.addr_to]
    
class NotificationDTO(BaseTranfer):
    chat_ids: list[int]
    transfer_type: TransferType
    user_address: str
    other_address: str
    balance: BalanceDTO
    wallet_name: str

    @property
    def other_wallet_role(self) -> str:
        return 'Recipient' if self.transfer_type == TransferType.Send else 'Sender'