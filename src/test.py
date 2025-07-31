from integrations.transactions.utils.expressions import ExpressionMaker
from core.networks import Networks
from services.webhook_service import WebhookService
from db.core.unit_of_work import UnitOfWork

import asyncio

async def main():
    await WebhookService(Networks.TRC20.value).update_webhook_addresses([
  "TSTR3hN7sowCkAHDpYQ62rrFR8A4ctwFr3",
  "TNVYYuFWP4ipSRMocVf4KLC1gv7vgJc3Vo",
  "TGNZB66dRenzkHSZKAKvDk6Kwpcd6s7fRm",
  "TWk7BYBFnV3jqfgmXzqV1ozRK2FF6GdKW6",
  "TTUogoyWexj9XaSxLpwkKnGSM7jmNWbyss",
  "TNTpcna8Bkp8WaPwYzGybDLStdjXvbhgvR"
]
)


if __name__ == '__main__':
    asyncio.run(main())