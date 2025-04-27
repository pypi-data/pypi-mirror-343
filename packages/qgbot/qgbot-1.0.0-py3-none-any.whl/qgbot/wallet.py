import logging
from decimal import Decimal
from .utils import get_eth_balance, now_price

class DynamicWallet:
    def __init__(self, config):
        self.config = config

    def fetch_live_tokens(self):
        try:
            eth_balance = get_eth_balance(self.config['wallet_address'])
            eth_price = now_price()

            if eth_balance == 0 or eth_price == 0:
                logging.warning("[WALLET WARNING] ETH balance or price returned zero.")

            portfolio = {
                'ETH': {
                    'balance': eth_balance,
                    'usd_value': eth_balance * eth_price
                }
            }
            return portfolio
        except Exception as e:
            logging.error(f"[WALLET ERROR] {e}")
            return {
                'ETH': {
                    'balance': Decimal('0'),
                    'usd_value': Decimal('0')
                }
            }
