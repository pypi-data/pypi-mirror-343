import logging
import time
import random
from decimal import Decimal, InvalidOperation
from typing import Dict, Any, Optional

from .utils import get_eth_balance, now_price, safe_rpc

class DynamicWallet:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.address: str = config.get('wallet_address', '')
        if not self.address:
            logging.critical("[WALLET INIT ERROR] No wallet address provided in config.")
            raise SystemExit(1)
        logging.info(f"[WALLET] Initialized for address: {self.address}")

    def fetch_live_tokens(self) -> Dict[str, Dict[str, Decimal]]:
        try:
            eth_balance = self._retry_fetch(self._get_eth_balance)
            eth_price = self._retry_fetch(self._get_now_price)
            usd_balance = eth_balance * eth_price

            token_balances = {
                'ETH': {
                    'balance': eth_balance,
                    'usd_value': usd_balance
                }
            }

            if self.config.get('track_tokens', False):
                token_list = self.config.get('token_contracts', [])
                for token in token_list:
                    entry = self._fetch_token_entry(token)
                    if entry:
                        token_balances.update(entry)

            return token_balances

        except Exception as e:
            logging.error(f"[WALLET FETCH ERROR] {e}")
            return self._empty_portfolio()

    def _retry_fetch(self, func, retries: int = 3, delay: int = 2) -> Decimal:
        for attempt in range(retries):
            try:
                result = func()
                if isinstance(result, Decimal) and result >= 0:
                    return result
                raise ValueError(f"Invalid result {result}")
            except (Exception, InvalidOperation) as e:
                logging.error(f"[RETRY {attempt+1}] {e}")
                time.sleep(delay + random.uniform(0, 1))
                delay *= 2
        logging.error(f"[FETCH ERROR] Max retries exceeded for {func.__name__}")
        return Decimal('0')

    def _get_eth_balance(self) -> Decimal:
        balance = get_eth_balance(self.address)
        return Decimal(balance)

    def _get_now_price(self) -> Decimal:
        price = now_price()
        return Decimal(price)

    def _fetch_token_entry(self, token: Dict[str, Any]) -> Optional[Dict[str, Dict[str, Decimal]]]:
        try:
            contract_address = token.get('address')
            decimals = token.get('decimals', 18)
            symbol = token.get('symbol', 'UNKNOWN')

            if not contract_address:
                logging.warning(f"[TOKEN DATA] Missing contract address for {symbol}. Skipping...")
                return None

            data = safe_rpc('eth_call', [{
                "to": contract_address,
                "data": "0x70a08231000000000000000000000000" + self.address[2:]
            }, "latest"])

            if not data:
                logging.warning(f"[TOKEN DATA] Empty response for {symbol}.")
                return None

            raw_balance = int(data, 16)
            token_balance = Decimal(raw_balance) / (Decimal(10) ** decimals)

            if token_balance == 0:
                return None

            token_price = self._retry_fetch(self._get_now_price)  # Placeholder until external oracle support
            token_usd_value = token_balance * token_price

            return {
                symbol: {
                    'balance': token_balance,
                    'usd_value': token_usd_value
                }
            }
        except Exception as e:
            logging.error(f"[TOKEN FETCH ERROR] {e}")
            return None

    def _empty_portfolio(self) -> Dict[str, Dict[str, Decimal]]:
        return {
            'ETH': {
                'balance': Decimal('0'),
                'usd_value': Decimal('0')
            }
        }