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
        self.config = self._load_config(config_path)
        set_config(self.config)  # Apply globally

        self.wallet = DynamicWallet(self.config)
        self.executor = TradeExecutor(self.wallet, self.config)
        self.gridbot = GridBot(self.wallet, self.executor, self.config)
        self.rebalancer = RebalanceBot(self.wallet, self.executor, self.config)

        self._threads = []
        self._running = False

    def _load_config(self, path):
        try:
            with open(path) as f:
                config = json.load(f)
            logging.info(f"[CONFIG] Loaded from {path}")
            return config
        except Exception as e:
            logging.critical(f"[CONFIG LOAD ERROR] {e}")
            raise SystemExit(1)

    def start_all(self):
        if self._running:
            logging.warning("[MASTER] Already running.")
            return

        self._running = True

        grid_thread = threading.Thread(target=self.gridbot.run, daemon=True)
        rebalance_thread = threading.Thread(target=self.rebalancer.run, daemon=True)

        grid_thread.start()
        rebalance_thread.start()

        self._threads = [grid_thread, rebalance_thread]

        logging.info("[MASTER] GridBot and RebalanceBot threads started.")

    def stop_all(self):
        if not self._running:
            logging.warning("[MASTER] Not running.")
            return

        self._running = False
        self.gridbot.stop()
        self.rebalancer.stop()

        for thread in self._threads:
            if thread and thread.is_alive():
                thread.join()

        logging.info("[MASTER] All bots shut down cleanly.")

    def run_forever(self):
        try:
            self.start_all()
            logging.info("[MASTER] Running indefinitely... (CTRL+C to stop)")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.warning("[MASTER] KeyboardInterrupt received.")
            self.stop_all()
        except Exception as e:
            logging.error(f"[MASTER ERROR] {e}")
            self.stop_all()