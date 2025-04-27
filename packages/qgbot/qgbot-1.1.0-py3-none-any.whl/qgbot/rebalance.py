import time
import logging
from decimal import Decimal
from .utils import now_price

class RebalanceBot:
    def __init__(self, wallet, executor, interval=180, fallback_sleep=10, rebalance_threshold=0.1, target_eth_ratio=0.5):
        """
        wallet: Wallet instance with fetch_live_tokens()
        executor: TradeExecutor instance to perform swaps
        interval: Main loop interval in seconds
        fallback_sleep: Sleep time after errors
        rebalance_threshold: % deviation from target ETH portfolio ratio to trigger rebalance
        target_eth_ratio: Ideal ETH holding ratio (default 50%)
        """
        self.wallet = wallet
        self.executor = executor
        self.interval = interval
        self.fallback_sleep = fallback_sleep
        self.rebalance_threshold = Decimal(str(rebalance_threshold))
        self.target_eth_ratio = Decimal(str(target_eth_ratio))
        self._running = True

    def stop(self):
        """Gracefully stop the rebalance loop."""
        self._running = False

    def run(self):
        """Main rebalance loop."""
        logging.info("[REBALANCER] Starting RebalanceBot...")
        while self._running:
            try:
                portfolio = self.wallet.fetch_live_tokens()

                eth_value = Decimal(portfolio.get('ETH', {}).get('usd_value', 0))
                total_value = sum(Decimal(asset.get('usd_value', 0)) for asset in portfolio.values())

                if eth_value == 0 or total_value == 0:
                    logging.warning("[REBALANCER WARNING] ETH or Total Portfolio value missing.")
                else:
                    eth_ratio = eth_value / total_value
                    logging.info(f"[REBALANCE] ETH ${eth_value:.2f} / Total ${total_value:.2f} (ETH {eth_ratio:.2%})")

                    deviation = abs(eth_ratio - self.target_eth_ratio)
                    if deviation > self.rebalance_threshold:
                        self.rebalance(eth_value, total_value, eth_ratio)

                time.sleep(self.interval)

            except Exception as e:
                logging.error(f"[REBALANCE ERROR] {e}")
                time.sleep(self.fallback_sleep)

    def rebalance(self, eth_value, total_value, eth_ratio):
        """Perform real rebalance."""
        try:
            target_eth_value = total_value * self.target_eth_ratio
            delta_value = target_eth_value - eth_value

            logging.info(f"[REBALANCER] Rebalance needed. Δ ${delta_value:.2f}")

            if delta_value > 0:
                # Need more ETH (BUY ETH)
                amount_to_swap = delta_value
                best_token = self.find_best_token_to_sell(exclude=['ETH'])
                if best_token:
                    logging.info(f"[REBALANCER] Swapping {best_token} → ETH (${amount_to_swap:.2f})")
                    self.executor.swap_to_eth(best_token, amount_to_swap)
            else:
                # Excess ETH, SELL ETH
                amount_to_sell = abs(delta_value)
                logging.info(f"[REBALANCER] Swapping ETH → USDC (${amount_to_sell:.2f})")
                self.executor.swap_eth_to_stable(amount_to_sell)

        except Exception as e:
            logging.error(f"[REBALANCE EXECUTION ERROR] {e}")

    def find_best_token_to_sell(self, exclude=None):
        """Finds the best non-ETH token to swap (largest USD value)."""
        try:
            portfolio = self.wallet.fetch_live_tokens()
            candidates = {k: v['usd_value'] for k, v in portfolio.items() if k not in (exclude or [])}

            if not candidates:
                logging.warning("[REBALANCER] No tokens to sell for rebalancing.")
                return None

            best_token = max(candidates, key=candidates.get)
            logging.info(f"[REBALANCER] Best token to sell: {best_token}")
            return best_token

        except Exception as e:
            logging.error(f"[FIND BEST TOKEN ERROR] {e}")
            return None