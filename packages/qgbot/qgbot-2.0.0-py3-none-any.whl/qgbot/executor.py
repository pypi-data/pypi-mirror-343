import time
import json
import logging
import random
import threading
import requests
from decimal import Decimal, InvalidOperation
from hashlib import sha3_256
from ecdsa import SigningKey, SECP256k1
from typing import Dict, Optional, Any

from .utils import (
    safe_rpc, get_eth_balance, get_gas_price, now_price,
    get_nonce, eth_to_tokens, tokens_to_eth, rlp_encode
)
from .scorer import TokenScorer
from .db import log_trade

class TradeExecutor:
    def __init__(self, wallet, config: Dict[str, Any]) -> None:
        self.wallet = wallet
        self.config = config
        self.token_scorer = TokenScorer(config.get("target_tokens", []))
        self.stop_event = threading.Event()

    def sign_tx(self, tx: Dict[str, Any], private_key_hex: str) -> Optional[str]:
        try:
            private_key_bytes = bytes.fromhex(private_key_hex.replace('0x', ''))
            sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)

            unsigned = [
                tx['nonce'], tx['gasPrice'], tx['gas'],
                bytes.fromhex(tx['to'][2:]), tx['value'],
                tx['data'], tx['chainId'], 0, 0
            ]
            rlp_unsigned = rlp_encode(unsigned)
            tx_hash = sha3_256(rlp_unsigned).digest()

            sig = sk.sign_digest(tx_hash, sigencode=lambda r, s, _: r.to_bytes(32, 'big') + s.to_bytes(32, 'big'))
            r, s = int.from_bytes(sig[:32], 'big'), int.from_bytes(sig[32:], 'big')
            v = tx['chainId'] * 2 + 35 + (1 if s % 2 != 0 else 0)

            signed = [
                tx['nonce'], tx['gasPrice'], tx['gas'],
                bytes.fromhex(tx['to'][2:]), tx['value'],
                tx['data'], v, r, s
            ]
            raw_tx = rlp_encode(signed)
            return '0x' + raw_tx.hex()
        except Exception as e:
            logging.error(f"[SIGN TX ERROR] {e}")
            return None

    def send_tx(self, signed_tx_hex: str) -> Optional[str]:
        retries = 3
        delay = 2
        fallback_used = False

        for attempt in range(retries):
            try:
                rpc_url = self.config['rpc_url']
                if fallback_used and 'secondary_rpc_url' in self.config:
                    rpc_url = self.config['secondary_rpc_url']

                payload = {
                    "jsonrpc": "2.0",
                    "method": "eth_sendRawTransaction",
                    "params": [signed_tx_hex],
                    "id": 1
                }
                response = requests.post(rpc_url, json=payload, headers={'Content-Type': 'application/json'}, timeout=10)
                response.raise_for_status()
                result = response.json()

                if 'error' in result:
                    raise Exception(result['error'])

                return result.get('result')
            except Exception as e:
                logging.error(f"[SEND TX RETRY {attempt+1}] {e}")
                time.sleep(delay + random.uniform(0, 1))
                delay *= 2
                fallback_used = True

        logging.error("[SEND TX ERROR] Max retries exceeded.")
        return None
        
        def wait_for_receipt(self, tx_hash: str, tx: Optional[Dict[str, Any]] = None, timeout: int = 60) -> Optional[Dict[str, Any]]:
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                receipt = safe_rpc("eth_getTransactionReceipt", [tx_hash])
                if receipt:
                    logging.info(f"[RECEIPT] TX {tx_hash[:12]}... confirmed.")
                    return receipt
                time.sleep(5)
            except Exception as e:
                logging.error(f"[RECEIPT FETCH ERROR] {e}")
                time.sleep(5)

        logging.error(f"[RECEIPT TIMEOUT] TX {tx_hash[:12]} not confirmed within {timeout}s.")
        if tx:
            return self.rebid_gas_and_resend(tx, tx_hash)
        return None

    def rebid_gas_and_resend(self, tx: Dict[str, Any], previous_tx_hash: str) -> Optional[str]:
        try:
            logging.warning(f"[REBID] Rebidding gas for stuck TX {previous_tx_hash[:12]}...")
            new_gas_price = int(Decimal(tx['gasPrice']) * Decimal('1.25'))
            tx['gasPrice'] = new_gas_price

            new_signed = self.sign_tx(tx, self.config['private_key'])
            if not new_signed:
                logging.error("[REBID ERROR] Failed to re-sign TX.")
                return None

            new_tx_hash = self.send_tx(new_signed)
            if new_tx_hash:
                self.wait_for_receipt(new_tx_hash)
                logging.info(f"[REBID SUCCESS] New TX {new_tx_hash[:12]} sent.")
                return new_tx_hash
        except Exception as e:
            logging.error(f"[REBID FAILURE] {e}")
            return None

    def safe_get_price(self, token: Optional[str] = None) -> Decimal:
        for attempt in range(3):
            try:
                price = now_price(token) if token else now_price()
                return Decimal(price)
            except (Exception, InvalidOperation) as e:
                logging.error(f"[PRICE FETCH RETRY {attempt+1}] {e}")
                time.sleep(2 * (2 ** attempt))
        logging.error("[PRICE FETCH ERROR] Max retries exceeded.")
        return Decimal('0')

    def safe_get_balance(self, address: str) -> Decimal:
        for attempt in range(3):
            try:
                return Decimal(get_eth_balance(address))
            except (Exception, InvalidOperation) as e:
                logging.error(f"[BALANCE FETCH RETRY {attempt+1}] {e}")
                time.sleep(2 * (2 ** attempt))
        logging.error("[BALANCE FETCH ERROR] Max retries exceeded.")
        return Decimal('0')

    def safe_get_nonce(self, address: str) -> Optional[int]:
        for attempt in range(3):
            try:
                return get_nonce(address)
            except Exception as e:
                logging.error(f"[NONCE FETCH RETRY {attempt+1}] {e}")
                time.sleep(2 * (2 ** attempt))
        logging.error("[NONCE FETCH ERROR] Max retries exceeded.")
        return None

    def gas_estimate_safe(self) -> int:
        try:
            gas_price = Decimal(get_gas_price())
            gas_price_buffered = int(gas_price * Decimal('1.20'))
            return gas_price_buffered
        except Exception as e:
            logging.error(f"[GAS FETCH ERROR] {e}")
            return int(Decimal('30000000000'))

    def check_slippage(self, expected_price: Decimal, actual_price: Decimal) -> bool:
        try:
            max_slippage = Decimal(str(self.config.get('max_slippage', 0.02)))
            allowed_diff = expected_price * max_slippage
            if abs(expected_price - actual_price) > allowed_diff:
                logging.warning(f"[SLIPPAGE] Expected {expected_price:.6f} vs Actual {actual_price:.6f} exceeds allowed {allowed_diff:.6f}")
                return False
            return True
        except Exception as e:
            logging.error(f"[SLIPPAGE CHECK ERROR] {e}")
            return False

    def batch_send_transactions(self, signed_tx_list: list[str]) -> None:
        def send_one(tx_hex):
            tx_hash = self.send_tx(tx_hex)
            if tx_hash:
                self.wait_for_receipt(tx_hash)

        threads = []
        for signed_tx in signed_tx_list:
            t = threading.Thread(target=send_one, args=(signed_tx,), daemon=True)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
            
        def execute_trade(self, adaptive_volume: Decimal = Decimal('1.0')) -> None:
        if self.stop_event.is_set():
            logging.warning("[EXECUTE TRADE] Stop event triggered. Aborting.")
            return

        try:
            eth_balance = self.safe_get_balance(self.config['wallet_address'])
            gas_price = self.gas_estimate_safe()
            gas_cost_eth = Decimal(gas_price * self.config['gas_limit']) / Decimal('1e18')
            available_balance = eth_balance - gas_cost_eth

            if available_balance <= Decimal('0.001'):
                logging.warning(f"[NO FUNDS] {eth_balance:.6f} ETH too low after gas.")
                return

            expected_price = self.safe_get_price()
            if expected_price == 0:
                logging.warning("[PRICE FETCH ZERO] Abort trade.")
                return

            trade_eth = min(Decimal(str(self.config['trade_volume'])) * adaptive_volume, available_balance)
            if trade_eth <= Decimal('0.001'):
                logging.warning(f"[SKIP] Final trade {trade_eth:.6f} ETH too small.")
                return

            value_wei = int(trade_eth * Decimal('1e18'))
            nonce = self.safe_get_nonce(self.config['wallet_address'])
            if nonce is None:
                logging.error("[EXECUTE TRADE ERROR] Nonce unavailable.")
                return

            token_out = self.token_scorer.best_token()
            deadline = int(time.time()) + 600
            data = eth_to_tokens(
                min_tokens_out=self.config['min_tokens_out'],
                path=[self.config['weth_address'], token_out],
                to=self.config['wallet_address'],
                deadline=deadline
            )

            actual_price = self.safe_get_price()
            if not self.check_slippage(expected_price, actual_price):
                logging.warning("[ABORT] Slippage exceeded on trade.")
                return

            tx = {
                "nonce": nonce,
                "gasPrice": gas_price,
                "gas": self.config['gas_limit'],
                "to": self.config['uniswap_router'],
                "value": value_wei,
                "data": data,
                "chainId": 1
            }

            signed = self.sign_tx(tx, self.config['private_key'])
            if signed:
                if self.config.get('simulate', False):
                    logging.info(f"[SIMULATE] Would SWAP {trade_eth:.6f} ETH → {token_out[:8]}...")
                    return

                tx_hash = self.send_tx(signed)
                if tx_hash:
                    self.wait_for_receipt(tx_hash, tx)
                    logging.info(f"[SWAP SUCCESS] TX {tx_hash[:12]} confirmed.")
                    log_trade(
                        time.strftime('%Y-%m-%d %H:%M:%S'),
                        "SWAP",
                        tx_hash,
                        float(actual_price),
                        float(trade_eth)
                    )
        except Exception as e:
            logging.error(f"[EXECUTE TRADE ERROR] {e}")

    def swap_to_eth(self, token_address: str, usd_amount: Decimal) -> None:
        if self.stop_event.is_set():
            logging.warning("[SWAP TO ETH] Stop event triggered. Aborting.")
            return

        try:
            expected_price = self.safe_get_price(token_address)
            if expected_price == 0:
                logging.warning("[TOKEN PRICE ZERO] Cannot swap.")
                return

            token_amount = Decimal(usd_amount) / expected_price
            token_amount_wei = int(token_amount * Decimal('1e18'))
            nonce = self.safe_get_nonce(self.config['wallet_address'])
            if nonce is None:
                logging.error("[SWAP TO ETH ERROR] Nonce unavailable.")
                return

            gas_price = self.gas_estimate_safe()
            deadline = int(time.time()) + 600
            data = tokens_to_eth(
                amount_in=token_amount_wei,
                amount_out_min=self.config['min_eth_out'],
                path=[token_address, self.config['weth_address']],
                to=self.config['wallet_address'],
                deadline=deadline
            )

            actual_price = self.safe_get_price(token_address)
            if not self.check_slippage(expected_price, actual_price):
                logging.warning("[ABORT] Slippage exceeded on token to ETH swap.")
                return

            tx = {
                "nonce": nonce,
                "gasPrice": gas_price,
                "gas": self.config['gas_limit'],
                "to": self.config['uniswap_router'],
                "value": 0,
                "data": data,
                "chainId": 1
            }

            signed = self.sign_tx(tx, self.config['private_key'])
            if signed:
                if self.config.get('simulate', False):
                    logging.info(f"[SIMULATE] Would SWAP {usd_amount:.2f} USD worth of token to ETH...")
                    return

                tx_hash = self.send_tx(signed)
                if tx_hash:
                    self.wait_for_receipt(tx_hash, tx)
                    logging.info(f"[TOKEN → ETH SUCCESS] TX {tx_hash[:12]} confirmed.")
                    log_trade(
                        time.strftime('%Y-%m-%d %H:%M:%S'),
                        "SWAP_TO_ETH",
                        tx_hash,
                        float(actual_price),
                        float(token_amount)
                    )
        except Exception as e:
            logging.error(f"[SWAP TO ETH ERROR] {e}")

    def swap_eth_to_stable(self, usd_amount: Decimal) -> None:
        if self.stop_event.is_set():
            logging.warning("[SWAP ETH TO STABLE] Stop event triggered. Aborting.")
            return

        try:
            expected_price = self.safe_get_price()
            if expected_price == 0:
                logging.warning("[PRICE ZERO] Cannot swap ETH to stable.")
                return

            eth_amount = Decimal(usd_amount) / expected_price
            eth_needed_wei = int(eth_amount * Decimal('1e18'))
            nonce = self.safe_get_nonce(self.config['wallet_address'])
            if nonce is None:
                logging.error("[SWAP ETH TO STABLE ERROR] Nonce unavailable.")
                return

            gas_price = self.gas_estimate_safe()
            deadline = int(time.time()) + 600
            data = eth_to_tokens(
                min_tokens_out=self.config['min_tokens_out'],
                path=[self.config['weth_address'], self.config['stablecoin_address']],
                to=self.config['wallet_address'],
                deadline=deadline
            )

            actual_price = self.safe_get_price()
            if not self.check_slippage(expected_price, actual_price):
                logging.warning("[ABORT] Slippage exceeded on ETH to stable swap.")
                return

            tx = {
                "nonce": nonce,
                "gasPrice": gas_price,
                "gas": self.config['gas_limit'],
                "to": self.config['uniswap_router'],
                "value": eth_needed_wei,
                "data": data,
                "chainId": 1
            }

            signed = self.sign_tx(tx, self.config['private_key'])
            if signed:
                if self.config.get('simulate', False):
                    logging.info(f"[SIMULATE] Would SWAP {eth_amount:.6f} ETH to STABLE...")
                    return

                tx_hash = self.send_tx(signed)
                if tx_hash:
                    self.wait_for_receipt(tx_hash, tx)
                    logging.info(f"[ETH → STABLE SUCCESS] TX {tx_hash[:12]} confirmed.")
                    log_trade(
                        time.strftime('%Y-%m-%d %H:%M:%S'),
                        "SWAP_TO_STABLE",
                        tx_hash,
                        float(actual_price),
                        float(eth_amount)
                    )
        except Exception as e:
            logging.error(f"[SWAP ETH TO STABLE ERROR] {e}")