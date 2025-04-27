import logging
import threading
from .wallet import DynamicWallet
from .executor import TradeExecutor
from .grid import GridBot
from .rebalance import RebalanceBot

class MasterController:
    def __init__(self):
        self.wallet = DynamicWallet()
        self.executor = TradeExecutor(self.wallet)
        self.gridbot = GridBot(self.wallet, self.executor)
        self.rebalancer = RebalanceBot(self.wallet, self.executor)

    def start_all(self):
        logging.info("[MASTER] Starting Intelligent Quant GridBot...")
        threading.Thread(target=self.gridbot.run, daemon=True).start()
        threading.Thread(target=self.rebalancer.run, daemon=True).start()
