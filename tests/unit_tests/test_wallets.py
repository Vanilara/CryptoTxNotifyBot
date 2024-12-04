import pytest
from src.integrations.wallets.balances_networks.erc import BalanceGetterERC
from src.integrations.wallets.balances_networks.trc import BalanceGetterTRC
from src.integrations.wallets.validator import WalletValidator
from src.core.networks import Networks


class TestBalanceGetterERC:
    @pytest.mark.asyncio
    @pytest.mark.parametrize('addresses', [
        (
            {
                '0x3451B6b219478037a1AC572706627FC2BDa1e812': True,
                '0x35677cD282499b69d5B6784b4607DD6FBe453BB0': True,
                'gjredl': False
            }
        ),
    ])
    async def test_take_balances(self, addresses):
        res = await BalanceGetterERC().take_balances([x for x in addresses])
        for row in res:
            assert row.is_validated == addresses[row.address]
        assert type(res) == list

class TestBalanceGetterTRC:
    @pytest.mark.asyncio
    @pytest.mark.parametrize('addresses', [
        ({
            'TSTR3hN7sowCkAHDpYQ62rrFR8A4ctwFr3': True,
            'TSSmpgRyNVXpJ1AkckkR8gfTJk5B7gQgB9': True,
            'TUF9zALCb6vz2sxPiPoMqVVfSGs6Seag8g': True,
            'TQCYEZVTP6Hd7ZmgmYJ4ToChrwZkq4AcWj': True,
            'erdtjf': False
        }),
        ({
            'TSTR3hN7sowCkAHDpYQ62rrFR8A4ctwFr3': True,
        })
    ])
    async def test_take_balances(self, addresses):
        res = await BalanceGetterTRC().take_balances([x for x in addresses])
        for row in res:
            assert row.is_validated == addresses[row.address]

class TestWalletValidators:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'network, address, result', [
            (Networks.TRC20.value, 'TSTR3hN7sowCkAHDpYQ62rrFR8A4ctwFr3', True),
            (Networks.TRC20.value, 'TBi7UdMg', False),
            (Networks.ERC20.value, '0x3451B6b219478037a1AC572706627FC2BDa1e812', True),
            (Networks.ERC20.value, '0x38B7Fe1f', False)
        ]             
    )
    async def test_check_wallet_trc(self, network, address, result):
        assert await WalletValidator(network).check_wallet(address) == result