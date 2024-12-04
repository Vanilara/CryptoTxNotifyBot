import pytest
from src.db.core.unit_of_work import UnitOfWork
from src.schemas.users import UserPostDTO
from src.schemas.wallets import WalletPostDTO
from src.services.wallet_service import WalletService
from src.db.core.unit_of_work import UnitOfWork


@pytest.fixture
def user1() -> UserPostDTO:
    return UserPostDTO(
        user_id=235465,
        username='alexxxx',
        first_name='Alex'
    )

@pytest.fixture
def user2() -> UserPostDTO:
    return UserPostDTO(
        user_id=43572,
        username='maxxx',
        first_name='Maxim'
    )

@pytest.fixture
def erc_addresses() -> list[str]:
    return [
        '0x1f2F10D1C40777AE1Da742455c65828FF36Df387',
        '0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7',
        '0x6381272d2F6f5e2d70C23f71e398ec0E0F5CA32d',
        '0xBe410F28b18f9d5AD39B2f9D7780f7d145D73F0A',
        '0x6c48beD2a9824C68E3e4Bef801e4ff7B47131235'
    ]

@pytest.fixture
def trc_addresses() -> list[str]:
    return [
        'TSTR3hN7sowCkAHDpYQ62rrFR8A4ctwFr3',
        'TEYx6pg3gMxnK9nVJGkhJYgKN3AbjxgKGE',
        'TUF9zALCb6vz2sxPiPoMqVVfSGs6Seag8g',
        'TDEA1UnGUPETFiYs2uoZqjPjphJEaEGqTr',
        'TQCYEZVTP6Hd7ZmgmYJ4ToChrwZkq4AcWj'
    ]



