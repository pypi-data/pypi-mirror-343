import logging
import time
import signal
from .core import MasterController
from .db import TradeDatabase

class AppRunner:
    def __init__(self, config_path='config.json'):
        self.master = None
        self.db = None
        self.config_path = config_path
        self._running = True

    def start(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler()]
        )

        logging.info("[APP] Launching Quant-GridBot System...")

        self.db = TradeDatabase()  # Database will be available to bots if needed
        self.master = MasterController(self.config_path)

        self.master.start()

        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        self.run_forever()

    def run_forever(self):
        try:
            while self._running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.shutdown()
        except Exception as e:
            logging.error(f"[APP ERROR] {e}")
            self.shutdown()

    def handle_signal(self, sig, frame):
        logging.warning(f"[SIGNAL] Received {sig}. Initiating shutdown...")
        self.shutdown()

    def shutdown(self):
        if not self._running:
            return
        self._running = False

        logging.info("[APP] Stopping bots and closing resources...")

        if self.master:
            self.master.stop()
        if self.db:
            self.db.close()

        logging.info("[APP] Shutdown complete.")

def main():
    app = AppRunner()
    app.start()