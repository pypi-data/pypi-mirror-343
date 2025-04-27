import logging
import time
import signal
from .core import MasterController
from .db import TradeDatabase

class AppRunner:
    def __init__(self):
        self.master = None
        self.db = None
        self._running = True

    def start(self):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
        logging.info("[MASTER] Starting Quant-GridBot System...")

        self.db = TradeDatabase()
        self.master = MasterController(self.db)

        self.master.start_all()

        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        self.run()

    def run(self):
        try:
            while self._running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.shutdown()

    def handle_signal(self, sig, frame):
        logging.info(f"[MASTER] Signal {sig} received.")
        self.shutdown()

    def shutdown(self):
        if not self._running:
            return
        logging.info("[MASTER] Shutting down bots...")
        self._running = False
        if self.master:
            self.master.stop_all()
        if self.db:
            self.db.close()
        logging.info("[MASTER] Shutdown complete.")

def main():
    app = AppRunner()
    app.start()
