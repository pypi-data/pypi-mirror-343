import logging
import time
import signal

from .core import MasterController
from .db import TradeDatabase

class AppRunner:
    def __init__(self, config_path='config.json'):
        self.config_path = config_path
        self.master = None
        self.db = None
        self._running = True

    def start(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler()]
        )

        logging.info("[APP] Quant-GridBot starting...")

        self.db = TradeDatabase()
        self.master = MasterController(self.config_path)

        self.master.start_all()

        # Properly trap OS signals
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        self._run_forever()

    def _run_forever(self):
        try:
            while self._running:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.warning("[APP] KeyboardInterrupt received.")
            self.shutdown()
        except Exception as e:
            logging.error(f"[APP ERROR] {e}")
            self.shutdown()

    def handle_signal(self, sig, frame):
        logging.warning(f"[APP] Signal {sig} caught. Shutting down...")
        self.shutdown()

    def shutdown(self):
        if not self._running:
            return

        self._running = False
        logging.info("[APP] Shutting down GridBot and Rebalancer...")

        if self.master:
            self.master.stop_all()
        if self.db:
            self.db.close()

        logging.info("[APP] Shutdown complete. Exiting cleanly.")

def main():
    app = AppRunner()
    app.start()