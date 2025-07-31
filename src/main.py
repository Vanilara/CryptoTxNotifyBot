import logging

from fastapi import FastAPI, Request

from services.transaction_service import TransactionService
from db.core.unit_of_work import UnitOfWork
from core.config import settings
from utils import logger_setter


app = FastAPI()



@app.post("/new_transaction")
async def test_post(request: Request):
    logging.info(f'Got new transaction: {await request.json()}')
    transaction_service = TransactionService(UnitOfWork())
    for transaction in await request.json():
        try:
            time_data = request.headers.get('x-qn-timestamp')
            await transaction_service.handle_transactions(transaction, time_data)
        except Exception as e:
            logging.error("An error occurred while handling transactions", exc_info=True)
    return 'OK'