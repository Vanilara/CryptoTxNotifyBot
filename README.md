# Crypto Notifier Bot

Telegram bot for instant notifications about transactions on selected wallets. The bot utilizes webhooks from QuickNode and supports TRC20 and ERC20 wallets. It also allows users to query wallet balances (using QuickNode for ERC20 and Tronscan for TRC20).

## Features
* Supports TRC20/ERC20 wallets.
* Wallet balance inquiries.
* Webhook integration with QuickNode for transaction notifications.
* PostgreSQL database.

## .env
```
#General
MODE = The environment mode. Use PROD for production or DEV for development.

#Database
DB_HOST = Hostname of the PostgreSQL server.
DB_PORT = Port number for the PostgreSQL server.
DB_USER = Username for the PostgreSQL database.
DB_PASS = Password for the PostgreSQL database.
DB_NAME = Name of the PostgreSQL database.

#PgAdmin
PGADMIN_EMAIL = Email address for the PgAdmin login.
PGADMIN_PASS = Password for the PgAdmin login.

#Webhook
WEBHOOK_BASE_URL = The base URL for the webhook (http://localhost:8000).

#API Keys
QUICKNODE_API_KEY = API key for QuickNode integration.
QUICKNODE_ENDPOINT_URL = Endpoint URL for QuickNode. Add {chain} instead of blockchain name. (https://neat-proportionate-bush.{chain}.quiknode.pro/)
TRONSCAN_API_KEY = API key for interacting with TronScan.

#Telegram Bot
TOKEN = Telegram Bot API token.
```

## Installation
* Dev:
```bash
docker-compose up --profile dev --build #postgres, pgadmin
poetry install && poetry shell
python3 bot.py
uvicorn main:app --debug
```
* Prod:
```bash
docker-compose up --build #fastapi, aiogram, postgres
```


