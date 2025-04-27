import threading
import logging
import json
from pathlib import Path

from .utils import set_config
from .wallet import DynamicWallet
from .executor import TradeExecutor
from .grid import GridBot
from .rebalance import RebalanceBot

class MasterController:
    def __init__(self, config_path='config.json'):
        self.config = self.load_config(config_path)
        set_config(self.config)  # Apply global config
        
        self.wallet = DynamicWallet(self.config)
        self.executor = TradeExecutor(self.wallet, self.config)
        self.grid = GridBot(self.wallet, self.executor, self.config)
        self.rebalance = RebalanceBot(self.wallet, self.executor, self.config)

        self.grid_thread = None
        self.rebalance_thread = None
        self._running = False

    def load_config(self, path):
        try:
            with open(path) as f:
                config = json.load(f)
            logging.info(f"[CONFIG] Loaded {path}")
            return config
        except Exception as e:
            logging.critical(f"[CONFIG LOAD ERROR] {e}")
            raise SystemExit(1)

    def start(self):
        if self._running:
            logging.warning("[MASTER] Already running.")
            return
        
        self._running = True
        self.grid_thread = threading.Thread(target=self.grid.run, daemon=True)
        self.rebalance_thread = threading.Thread(target=self.rebalance.run, daemon=True)

        self.grid_thread.start()
        self.rebalance_thread.start()

        logging.info("[MASTER] Grid and Rebalance threads started.")

    def stop(self):
        if not self._running:
            logging.warning("[MASTER] Not running.")
            return
        
        self._running = False
        self.grid.stop()
        self.rebalance.stop()

        if self.grid_thread:
            self.grid_thread.join()
        if self.rebalance_thread:
            self.rebalance_thread.join()

        logging.info("[MASTER] All threads stopped cleanly.")

    def run_forever(self):
        """Blocking call to run system indefinitely."""
        try:
            self.start()
            while True:
                pass  # Idle; threads are running in background
        except KeyboardInterrupt:
            logging.warning("[MASTER] Keyboard interrupt received. Shutting down...")
            self.stop()
        except Exception as e:
            logging.error(f"[MASTER ERROR] {e}")
            self.stop()