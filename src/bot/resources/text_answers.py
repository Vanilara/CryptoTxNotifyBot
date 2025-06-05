from schemas.wallets import BalanceDTO, WalletDTO


class TextMsgs:
    CANCEL = "Cancelled"
    
    WALLET_ADD_NAME = 'How do you want to name your wallet?'
    WALLET_ADD_NETWORK = "What is your wallet's network?"
    WALLET_ADD_ADDRESS = "What is your wallet address?"

    WALLET_RENAMED = "Wallet title changed successfuly"

    ADDED_TO_GROUP = "Please continue message forwarding setup in private chat"

    GROUPS_INFO = "To receive bot messages in group chat follow these steps:\n\n1️⃣ First, add this bot to your private group chat.\n\n2️⃣ Second, choose your chat from the list below. Note that only groups are available, not supergroups nor channels.\n\n■ – bot will send messages to this group\n□ – bot will not send messages to this group"

    @staticmethod
    def welcome(name: str) -> str:
        return f"Welcome, {name} 👋\n\nI'm CryptoAlert bot and I can help you monitor your cryptocurrency wallets. Feel free to add your wallets and wait for messages from me!"
    
    @staticmethod
    def balances(balances: list[BalanceDTO]) -> str:
        if len(balances) == 0:
            return "🫤 You haven't added any wallets yet\n\nAdd your first wallet to view its balance"
        message = ''
        sum_amount = 0
        for balance in balances:
            message += f"<b>{balance.name}</b> - <i>{balance.network_user_name}</i>\n<pre>{balance.address}</pre>\n{balance.format_to_msg()}\n\n"
            sum_amount += balance.amount
        message += f'<b>TOTAL: {round(sum_amount, 2)} USDT</b>'
        return message
    
    @staticmethod
    def wallets(wallets: list[WalletDTO]) -> str:
        if len(wallets) == 0:
            return "🫤 You haven't added any wallets yet\n\nAdd your first wallet to get instant notifications about new transactions"
        message = ''
        for wallet in wallets:
            message += f"<b>{wallet.name}</b> - <i>{wallet.network_user_name}</i>\n<pre>{wallet.address}</pre>\n\n"
        return message

    @staticmethod
    def wallet(wallet: WalletDTO) -> str:
        if wallet.has_notifications:
            notifs_message = '🔔 You will receive a message every time the transaction occurs.'
        else:
            notifs_message = '🔕 You will not receive any messages about this wallet.'
        return f"Wallet <b>{wallet.name}</b>\nOnly <i>{wallet.network_user_name}</i> transactions are observed.\n<pre>{wallet.address}</pre>\n\n{notifs_message}\n\n👥 You can attach a group chat to this wallet so the bot will send messages about all transactions to this group chat too"
    
    @staticmethod
    def wallet_added(name: str) -> str:
        return f'👌 Wallet {name} saved!\n\nYou will receive messages about new transactions'
    
    @staticmethod
    def wallet_rename_set(name: str) -> str:
        return f'Choose new name for a wallet {name}'
    
    @staticmethod
    def wallet_deleted(name: str, network: str) -> str:
        return f"You deleted wallet {name} - {network}"