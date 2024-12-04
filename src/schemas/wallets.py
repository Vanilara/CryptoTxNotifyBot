from pydantic import BaseModel
from core.networks import Networks



class WalletPostDTO(BaseModel):
    user_id: int
    name: str
    network: str
    address: str

class WalletDTO(WalletPostDTO):
    id: int
    has_notifications: bool

    @property
    def network_user_name(self) -> str:
        return Networks.get_by_abbr(self.network).user_name

class WalletUpdateDTO(BaseModel):
    has_notifications: bool | None = None
    name: str | None = None

class BalanceDTO(BaseModel):
    network: str
    address: str
    is_validated: bool = True
    amount: float = 0
    name: str = ''

    def set_name(self, name) -> "BalanceDTO":
        self.name = name
        return self
    
    def format_to_msg(self) -> float | str:
        if not self.is_validated:
            return f"<i>Can't fetch balance now</i>"
        return f'{str(self.amount)} USDT'
    
    @property
    def network_user_name(self) -> str:
        return Networks.get_by_abbr(self.network).user_name