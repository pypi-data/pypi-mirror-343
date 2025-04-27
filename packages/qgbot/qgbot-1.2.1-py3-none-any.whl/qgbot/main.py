import logging
import time
import signal
import sys

from .core import MasterController
from .db import TradeDatabase

class AppRunner:
    def __init__(self, config_path='config.json'):
        self.config_path = config_path
        self.master = None
        self.db = None
        self._running = False

    def start(self):
        self._configure_logging()

        logging.info("[APP] Quant-GridBot starting...")

        try:
            self.db = TradeDatabase()
            self.master = MasterController(self.config_path)

            self._running = True
            self._attach_signals()

            self.master.start_all()
            self._run_forever()

        except Exception as e:
            logging.critical(f"[APP START FAILURE] {e}")
            self.shutdown()

    def _configure_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)]
        )

    def _attach_signals(self):
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

    def _run_forever(self):
        try:
            while self._running:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.warning("[APP] KeyboardInterrupt received.")
            self.shutdown()
        except Exception as e:
            logging.error(f"[APP MAIN LOOP ERROR] {e}")
            self.shutdown()

    def handle_signal(self, sig, frame):
        logging.warning(f"[APP] Signal {sig} caught. Initiating shutdown...")
        self.shutdown()

    def shutdown(self):
        if not self._running:
            return

        logging.info("[APP] Shutdown initiated...")
        self._running = False

        try:
            if self.master:
                self.master.stop_all()
            if self.db:
                self.db.close()
        except Exception as e:
            logging.error(f"[APP SHUTDOWN ERROR] {e}")

        logging.info("[APP] Shutdown complete. Exiting.")
        sys.exit(0)

def main():
    app = AppRunner()
    app.start()