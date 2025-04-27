import time
import logging
from .utils import now_price

class RebalanceBot:
    def __init__(self, wallet, executor, interval=180, fallback_sleep=10):
        self.wallet = wallet
        self.executor = executor
        self.interval = interval
        self.fallback_sleep = fallback_sleep
        self._running = True  # Internal control flag

    def stop(self):
        self._running = False

    def run(self):
        logging.info("[REBALANCER] Starting RebalanceBot...")
        while self._running:
            try:
                portfolio = self.wallet.fetch_live_tokens()

                eth_value = portfolio.get('ETH', {}).get('usd_value', 0)
                total_value = sum(asset.get('usd_value', 0) for asset in portfolio.values())

                if eth_value == 0 or total_value == 0:
                    logging.warning("[REBALANCER WARNING] Portfolio values zero or missing.")

                logging.info(f"[REBALANCE] ETH ${eth_value:.2f} / Total Portfolio ${total_value:.2f}")

                # Optionally, trigger rebalance action here if portfolio skew exceeds threshold (future enhancement)

                time.sleep(self.interval)
            except Exception as e:
                logging.error(f"[REBALANCE ERROR] {e}")
                time.sleep(self.fallback_sleep)
