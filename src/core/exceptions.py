class WalletUnvalidated(ValueError):
    def __init__(self):
        super().__init__(f"<b>The wallet address you sent is not valid for this token</b>\n\nPlease choose another address")

class ExpressionUnvalidated(ValueError):
    pass

class WalletNameTooLong(ValueError):
    def __init__(self):
        super().__init__(f"<b>This name is too long</b>\n\nPlease choose name that is not longer than 20 characters")

class WalletDuplicateName(ValueError):
    def __init__(self):
        super().__init__(f"<b>You already have wallet with this name</b>\n\nPlease choose another namet")

class WalletDuplicateAddress(ValueError):
    def __init__(self):
        super().__init__(f"<b>This address is already added to your wallets</b>\n\nPlease use another address to add new wallet")

class NoSuchAlert(ValueError):
    pass

class NoSuchWebhook(ValueError):
    pass

class DestinationHasAlerts(ValueError):
    pass

class NotOneDestination(ValueError):
    pass

class TooManyDestinations(ValueError):
    pass