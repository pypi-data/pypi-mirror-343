import logging
import time
import signal
import sys
from typing import Optional

from .core import MasterController
from .db import TradeDatabase

class AppRunner:
    def __init__(self, config_path: str = 'config.json') -> None:
        self.config_path: str = config_path
        self.master: Optional[MasterController] = None
        self.db: Optional[TradeDatabase] = None
        self._running: bool = False

    def start(self) -> None:
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
            self.shutdown(exit_code=1)

    def _configure_logging(self) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)]
        )

    def _attach_signals(self) -> None:
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

    def _run_forever(self) -> None:
        try:
            while self._running:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.warning("[APP] KeyboardInterrupt received.")
            self.shutdown(exit_code=0)
        except Exception as e:
            logging.error(f"[APP MAIN LOOP ERROR] {e}")
            self.shutdown(exit_code=1)

    def handle_signal(self, sig: int, frame: Optional[object]) -> None:
        logging.warning(f"[APP] Signal {sig} caught. Initiating shutdown...")
        self.shutdown(exit_code=0)

    def shutdown(self, exit_code: int = 0) -> None:
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
        sys.exit(exit_code)

def main() -> None:
    app = AppRunner()
    app.start()