import time
import logging
from decimal import Decimal
from .utils import now_price, safe_rpc

class RebalanceBot:
    def __init__(self, wallet, executor, config):
        self.wallet = wallet
        self.executor = executor
        self.config = config
        self.interval = config.get('refresh_interval', 180)
        self.fallback_sleep = config.get('fallback_sleep', 10)
        self.rebalance_threshold = Decimal(str(config.get('rebalance_threshold', 0.1)))
        self.target_eth_ratio = Decimal(str(config.get('target_eth_ratio', 0.5)))
        self._running = True

    def stop(self):
        self._running = False

    def run(self):
        logging.info("[REBALANCER] Running...")
        while self._running:
            try:
                eth_price = now_price()
                portfolio = self.wallet.fetch_live_tokens()

                eth_value = Decimal(portfolio.get('ETH', {}).get('usd_value', 0))
                total_value = sum(Decimal(asset.get('usd_value', 0)) for asset in portfolio.values())

                if eth_value <= 0 or total_value <= 0 or eth_price <= 0:
                    logging.warning("[REBALANCER WARNING] Invalid ETH or portfolio value detected.")
                else:
                    eth_ratio = eth_value / total_value
                    logging.info(f"[REBALANCE STATUS] ETH ${eth_value:.2f} / Total ${total_value:.2f} (ETH {eth_ratio:.2%})")

                    deviation = abs(eth_ratio - self.target_eth_ratio)
                    if deviation > self.rebalance_threshold:
                        self._rebalance(eth_value, total_value, eth_ratio, eth_price)

                time.sleep(self.interval)

            except Exception as e:
                logging.error(f"[REBALANCE LOOP ERROR] {e}")
                time.sleep(self.fallback_sleep)

    def _rebalance(self, eth_value, total_value, eth_ratio, eth_price):
        try:
            target_eth_value = total_value * self.target_eth_ratio
            delta_value = target_eth_value - eth_value

            logging.info(f"[REBALANCE ACTION] Target Δ ${delta_value:.2f}")

            if delta_value > 0:
                amount_needed = delta_value
                best_token = self._find_best_token_to_sell()
                if best_token:
                    logging.info(f"[REBALANCER] Swapping {best_token} → ETH (${amount_needed:.2f})...")
                    self.executor.swap_to_eth(best_token, amount_needed)
                else:
                    logging.warning("[REBALANCER] No sellable token found.")
            else:
                amount_to_sell = abs(delta_value)
                logging.info(f"[REBALANCER] Selling ETH → stablecoin (${amount_to_sell:.2f})...")
                self.executor.swap_eth_to_stable(amount_to_sell)

        except Exception as e:
            logging.error(f"[REBALANCE EXECUTION ERROR] {e}")

    def _find_best_token_to_sell(self):
        """Find largest non-ETH token dynamically via safe_rpc and live wallet fetch."""
        try:
            portfolio = self.wallet.fetch_live_tokens()
            candidates = {
                token: Decimal(asset.get('usd_value', 0))
                for token, asset in portfolio.items()
                if token != 'ETH' and Decimal(asset.get('usd_value', 0)) > 0
            }

            if not candidates:
                logging.warning("[REBALANCER] No alternative tokens available to rebalance.")
                return None

            best_token = max(candidates, key=candidates.get)
            logging.info(f"[REBALANCER] Selected {best_token} for rebalance.")
            return best_token

        except Exception as e:
            logging.error(f"[BEST TOKEN SELECTION ERROR] {e}")
            return None