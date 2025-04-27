import logging
import time
import random
from decimal import Decimal, InvalidOperation
from .utils import get_eth_balance, now_price, safe_rpc

class DynamicWallet:
    def __init__(self, config):
        self.config = config

    def fetch_live_tokens(self):
        try:
            address = self.config.get('wallet_address')
            if not address:
                logging.error("[WALLET CONFIG ERROR] Missing wallet address in config.")
                return self._empty_portfolio()

            eth_balance = self._safe_get_balance(address)
            eth_price = self._safe_now_price()

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

    def _safe_get_balance(self, address):
        retries = 3
        delay = 2
        for attempt in range(retries):
            try:
                balance = Decimal(get_eth_balance(address))
                if balance < 0:
                    raise ValueError("Negative balance fetched.")
                return balance
            except (Exception, InvalidOperation) as e:
                logging.error(f"[BALANCE FETCH RETRY {attempt+1}] {e}")
                time.sleep(delay + random.uniform(0, 1))
                delay *= 2
        logging.error("[BALANCE FETCH ERROR] Max retries exceeded.")
        return Decimal('0')

    def _safe_now_price(self):
        retries = 3
        delay = 2
        for attempt in range(retries):
            try:
                price = Decimal(now_price())
                if price < 0:
                    raise ValueError("Negative price fetched.")
                return price
            except (Exception, InvalidOperation) as e:
                logging.error(f"[PRICE FETCH RETRY {attempt+1}] {e}")
                time.sleep(delay + random.uniform(0, 1))
                delay *= 2
        logging.error("[PRICE FETCH ERROR] Max retries exceeded.")
        return Decimal('0')

    def _empty_portfolio(self):
        return {
            'ETH': {
                'balance': Decimal('0'),
                'usd_value': Decimal('0')
            }
        }