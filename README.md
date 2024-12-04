
```
crypto-notifier
├─ .DS_Store
├─ .dockerignore
├─ .env
├─ .gitignore
├─ .pytest_cache
│  ├─ .gitignore
│  ├─ CACHEDIR.TAG
│  ├─ README.md
│  └─ v
│     └─ cache
│        ├─ lastfailed
│        ├─ nodeids
│        └─ stepwise
├─ .vscode
│  └─ settings.json
├─ Dockerfile.base
├─ Dockerfile.bot
├─ Dockerfile.fastapi
├─ README.md
├─ alembic.ini
├─ data
│  └─ quicknode_state.json
├─ docker-compose.yaml
├─ logs
│  └─ logs.log
├─ poetry.lock
├─ pyproject.toml
├─ pytest.ini
├─ src
│  ├─ .DS_Store
│  ├─ __init__.py
│  ├─ __pycache__
│  │  ├─ __init__.cpython-313.pyc
│  │  └─ main.cpython-313.pyc
│  ├─ bot
│  │  ├─ __init__.py
│  │  ├─ __pycache__
│  │  │  └─ __init__.cpython-313.pyc
│  │  ├─ handlers
│  │  │  ├─ __init__.py
│  │  │  ├─ __pycache__
│  │  │  │  ├─ __init__.cpython-313.pyc
│  │  │  │  ├─ callbacks.cpython-313.pyc
│  │  │  │  ├─ menues.cpython-313.pyc
│  │  │  │  ├─ messages.cpython-313.pyc
│  │  │  │  └─ updates.cpython-313.pyc
│  │  │  ├─ callbacks.py
│  │  │  ├─ menues.py
│  │  │  ├─ messages.py
│  │  │  └─ updates.py
│  │  ├─ resources
│  │  │  ├─ __init__.py
│  │  │  ├─ __pycache__
│  │  │  │  ├─ __init__.cpython-313.pyc
│  │  │  │  ├─ callbacks_factory.cpython-313.pyc
│  │  │  │  ├─ filters.cpython-313.pyc
│  │  │  │  ├─ keyboards.cpython-313.pyc
│  │  │  │  ├─ states.cpython-313.pyc
│  │  │  │  └─ text_answers.cpython-313.pyc
│  │  │  ├─ callbacks_factory.py
│  │  │  ├─ filters.py
│  │  │  ├─ keyboards.py
│  │  │  ├─ states.py
│  │  │  └─ text_answers.py
│  │  └─ utils
│  │     ├─ __init__.py
│  │     ├─ __pycache__
│  │     │  └─ msg_sender.cpython-313.pyc
│  │     └─ msg_sender.py
│  ├─ bot.py
│  ├─ core
│  │  ├─ __init__.py
│  │  ├─ __pycache__
│  │  │  ├─ __init__.cpython-313.pyc
│  │  │  ├─ config.cpython-313.pyc
│  │  │  ├─ enums.cpython-313.pyc
│  │  │  ├─ exceptions.cpython-313.pyc
│  │  │  └─ networks.cpython-313.pyc
│  │  ├─ config.py
│  │  ├─ enums.py
│  │  ├─ exceptions.py
│  │  └─ networks.py
│  ├─ db
│  │  ├─ __init__.py
│  │  ├─ __pycache__
│  │  │  ├─ __init__.cpython-313.pyc
│  │  │  └─ connector.cpython-313.pyc
│  │  ├─ connector.py
│  │  ├─ core
│  │  │  ├─ __init__.py
│  │  │  ├─ __pycache__
│  │  │  │  ├─ __init__.cpython-313.pyc
│  │  │  │  ├─ base_model.cpython-313.pyc
│  │  │  │  ├─ base_repository.cpython-313.pyc
│  │  │  │  └─ unit_of_work.cpython-313.pyc
│  │  │  ├─ base_model.py
│  │  │  ├─ base_repository.py
│  │  │  └─ unit_of_work.py
│  │  ├─ migrations
│  │  │  ├─ env.py
│  │  │  ├─ script.py.mako
│  │  │  └─ versions
│  │  │     └─ ae7f0cc04b95_init.py
│  │  ├─ models
│  │  │  ├─ __init__.py
│  │  │  ├─ __pycache__
│  │  │  │  ├─ __init__.cpython-313.pyc
│  │  │  │  ├─ group_wallets.cpython-313.pyc
│  │  │  │  ├─ groups.cpython-313.pyc
│  │  │  │  ├─ users.cpython-313.pyc
│  │  │  │  └─ wallets.cpython-313.pyc
│  │  │  ├─ group_wallets.py
│  │  │  ├─ groups.py
│  │  │  ├─ users.py
│  │  │  └─ wallets.py
│  │  └─ repositories
│  │     ├─ __init__.py
│  │     ├─ __pycache__
│  │     │  ├─ __init__.cpython-313.pyc
│  │     │  ├─ groups.cpython-313.pyc
│  │     │  ├─ users.cpython-313.pyc
│  │     │  └─ wallets.cpython-313.pyc
│  │     ├─ groups.py
│  │     ├─ users.py
│  │     └─ wallets.py
│  ├─ integrations
│  │  ├─ __init__.py
│  │  ├─ __pycache__
│  │  │  ├─ __init__.cpython-313.pyc
│  │  │  ├─ base.cpython-313.pyc
│  │  │  └─ models.cpython-313.pyc
│  │  ├─ base.py
│  │  ├─ models.py
│  │  ├─ transactions
│  │  │  ├─ __init__.py
│  │  │  ├─ __pycache__
│  │  │  │  ├─ __init__.cpython-313.pyc
│  │  │  │  ├─ alerts.cpython-313.pyc
│  │  │  │  └─ destinations.cpython-313.pyc
│  │  │  ├─ alerts.py
│  │  │  ├─ destinations.py
│  │  │  └─ utils
│  │  │     ├─ __pycache__
│  │  │     │  └─ expressions.cpython-313.pyc
│  │  │     └─ expressions.py
│  │  └─ wallets
│  │     ├─ __init__.py
│  │     ├─ __pycache__
│  │     │  ├─ __init__.cpython-313.pyc
│  │     │  └─ validator.cpython-313.pyc
│  │     ├─ balances_networks
│  │     │  ├─ __init__.py
│  │     │  ├─ __pycache__
│  │     │  │  ├─ __init__.cpython-313.pyc
│  │     │  │  ├─ erc.cpython-313.pyc
│  │     │  │  └─ trc.cpython-313.pyc
│  │     │  ├─ erc.py
│  │     │  └─ trc.py
│  │     └─ validator.py
│  ├─ main.py
│  ├─ schemas
│  │  ├─ __init__.py
│  │  ├─ __pycache__
│  │  │  ├─ __init__.cpython-313.pyc
│  │  │  ├─ groups.cpython-313.pyc
│  │  │  ├─ transactions.cpython-313.pyc
│  │  │  ├─ transations.cpython-313.pyc
│  │  │  ├─ users.cpython-313.pyc
│  │  │  ├─ wallets.cpython-313.pyc
│  │  │  └─ webhooks.cpython-313.pyc
│  │  ├─ groups.py
│  │  ├─ transactions.py
│  │  ├─ users.py
│  │  ├─ wallets.py
│  │  └─ webhooks.py
│  ├─ services
│  │  ├─ __init__.py
│  │  ├─ __pycache__
│  │  │  ├─ __init__.cpython-313.pyc
│  │  │  ├─ balance_service.cpython-313.pyc
│  │  │  ├─ destination_service.cpython-313.pyc
│  │  │  ├─ group_service.cpython-313.pyc
│  │  │  ├─ transaction_service.cpython-313.pyc
│  │  │  ├─ user_service.cpython-313.pyc
│  │  │  ├─ wallet_service.cpython-313.pyc
│  │  │  └─ webhook_service.cpython-313.pyc
│  │  ├─ balance_service.py
│  │  ├─ destination_service.py
│  │  ├─ group_service.py
│  │  ├─ transaction_service.py
│  │  ├─ user_service.py
│  │  ├─ wallet_service.py
│  │  └─ webhook_service.py
│  ├─ utils
│  │  ├─ __init__.py
│  │  ├─ __pycache__
│  │  │  ├─ __init__.cpython-313.pyc
│  │  │  └─ logger_setter.cpython-313.pyc
│  │  ├─ files
│  │  │  ├─ __init__.py
│  │  │  ├─ __pycache__
│  │  │  │  ├─ __init__.cpython-313.pyc
│  │  │  │  └─ state_files_handler.cpython-313.pyc
│  │  │  └─ state_files_handler.py
│  │  ├─ hasher
│  │  │  ├─ __init__.py
│  │  │  ├─ __pycache__
│  │  │  │  ├─ __init__.cpython-313.pyc
│  │  │  │  ├─ addresses.cpython-313.pyc
│  │  │  │  └─ common.cpython-313.pyc
│  │  │  ├─ addresses.py
│  │  │  └─ common.py
│  │  └─ logger_setter.py
│  └─ webhook_setter.py
└─ tests
   ├─ __pycache__
   │  ├─ conftest.cpython-313-pytest-8.3.3.pyc
   │  └─ test_users.cpython-313-pytest-8.3.3.pyc
   ├─ conftest.py
   ├─ service_tests
   │  ├─ __init__.py
   │  ├─ __pycache__
   │  │  ├─ __init__.cpython-313.pyc
   │  │  ├─ conftest.cpython-313-pytest-8.3.3.pyc
   │  │  ├─ test_balance.cpython-313-pytest-8.3.3.pyc
   │  │  ├─ test_transactions.cpython-313-pytest-8.3.3.pyc
   │  │  ├─ test_user.cpython-313-pytest-8.3.3.pyc
   │  │  ├─ test_users.cpython-313-pytest-8.3.3.pyc
   │  │  └─ test_wallet.cpython-313-pytest-8.3.3.pyc
   │  ├─ conftest.py
   │  ├─ test_transactions.py
   │  ├─ test_user.py
   │  └─ test_wallet.py
   └─ unit_tests
      ├─ __pycache__
      │  ├─ test_transactions.cpython-313-pytest-8.3.3.pyc
      │  ├─ test_wallets.cpython-313-pytest-8.3.3.pyc
      │  └─ test_webhooks.cpython-313-pytest-8.3.3.pyc
      ├─ test_wallets.py
      └─ test_webhooks.py

```