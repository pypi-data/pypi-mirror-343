import logging
from decimal import Decimal
from .utils import get_eth_balance, now_price

class DynamicWallet:
    def __init__(self, config):
        self.config = config

    def fetch_live_tokens(self):
        try:
            address = self.config.get('wallet_address')
            if not address:
                logging.error("[WALLET CONFIG ERROR] Missing wallet address in config.")
                return self._empty_portfolio()

            eth_balance = Decimal(get_eth_balance(address))
            eth_price = Decimal(now_price())

            if eth_balance <= 0 or eth_price <= 0:
                logging.warning(f"[WALLET WARNING] Non-positive balance ({eth_balance}) or price ({eth_price}).")

            return {
                'ETH': {
                    'balance': eth_balance,
                    'usd_value': eth_balance * eth_price
                }
            }

        except Exception as e:
            logging.error(f"[WALLET FETCH ERROR] {e}")
            return self._empty_portfolio()

    def _empty_portfolio(self):
        return {
            'ETH': {
                'balance': Decimal('0'),
                'usd_value': Decimal('0')
            }
        }