wallet_manager = None
user_manager = None
coin_manager = None
transaction_manager = None
explorer_manager = None

def initialize(api_key: str):
    """
    Initialize the DNet library with the given API key.
    This must be called once before importing the managers.
    """
    global wallet_manager, user_manager, coin_manager, transaction_manager, explorer_manager
    from .manager_factory import DNetManager
    dnet_manager = DNetManager(api_key)
    wallet_manager = dnet_manager.get_wallet_manager()
    user_manager = dnet_manager.get_user_manager()
    coin_manager = dnet_manager.get_coin_manager()
    transaction_manager = dnet_manager.get_transaction_manager()
    explorer_manager = dnet_manager.get_explorer_manager()
    