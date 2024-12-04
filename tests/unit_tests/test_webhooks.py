import pytest

from src.core.exceptions import DestinationHasAlerts
from src.integrations.transactions.alerts import AlertsManager
from src.integrations.transactions.destinations import DestinationManager
from src.integrations.transactions.utils.expressions import ExpressionMaker
from src.core.networks import Networks


server_url = 'https://9329-2405-9800-b970-69eb-c90a-4b84-65d4-9f28.ngrok-free.app'

@pytest.fixture(scope='module', autouse=True)
async def setup_destination():
    yield
    try:
        await DestinationManager().delete_main()
    except DestinationHasAlerts:
        pass

class TestExpressionMaker:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'network, addresses, result', [
            (
                Networks.TRC20.value, [
                    'TCUF5G1h67ZtH1Qc7KdnHJzDnxBcXjVjsP',
                    'TSTR3hN7sowCkAHDpYQ62rrFR8A4ctwFr3'
                ],
                True
            ),
            (
                Networks.TRC20.value, [
                    'TSTR3hN7sowCkAHDpYQ62rrFR8A4ctwFr3'
                ],
                True
            ),
            (
                Networks.ERC20.value, [
                    '0x38B7Fe1f8Af3B8768cdF82E3Ac7f5d7b3a192Eb3',
                    '0x3451B6b219478037a1AC572706627FC2BDa1e812'
                ],
                True
            )

        ]
    )
    async def test_make_expression(self, network, addresses, result):
        expression = ExpressionMaker.make_expression(network, addresses)
        res = await AlertsManager(network).validate_expression(expression.hashed)
        assert res == result

class TestDestinationManager:
    @pytest.mark.asyncio
    async def test_create(self):
        manager = DestinationManager()
        created_id = await manager.create(server_url)
        assert await manager.get_main_one() == created_id

class TestAlertsManager:
    @pytest.mark.asyncio()
    @pytest.mark.parametrize(
        'network, addresses_to_make, addresses_to_update', [
            (
                Networks.TRC20.value,
                ['TCUF5G1h67ZtH1Qc7KdnHJzDnxBcXjVjsP'],
                ['TCUF5G1h67ZtH1Qc7KdnHJzDnxBcXjVjsP', 'TUF9zALCb6vz2sxPiPoMqVVfSGs6Seag8g']
            ),
            (
                Networks.ERC20.value,
                ['0x1f2F10D1C40777AE1Da742455c65828FF36Df387'],
                ['0x1f2F10D1C40777AE1Da742455c65828FF36Df387', '0x5F094191DDad05c5B6DDFA992A4F49d8d679290d']
            )
        ]
    )
    async def test_creating_updating(self, network, addresses_to_make, addresses_to_update):
        manager = AlertsManager(network)

        for alert in await manager.get_all():
            await manager.delete_by_id(alert['id'])
        assert await manager.get_all() == []

        create_expression = ExpressionMaker.make_expression(network, addresses_to_make).hashed
        update_expression = ExpressionMaker.make_expression(network, addresses_to_update).hashed
        for expr in (create_expression, update_expression):
            assert await manager.validate_expression(expr) == True

        alert_id = await manager.create(
            expression=create_expression,
            destination_id = await DestinationManager().create(server_url)
        )
        assert len(await manager.get_all()) == 1

        await manager.update(
            alert_id = alert_id['id'],
            expression = update_expression
        )
        assert len(await manager.get_all()) == 1
        


