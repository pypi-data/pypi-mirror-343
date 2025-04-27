import time
import json
import logging
import urllib.request
from decimal import Decimal
from hashlib import sha3_256
from ecdsa import SigningKey, SECP256k1

from .utils import get_eth_balance, get_gas_price, now_price, get_nonce, encode_swap_exact_eth_for_tokens, rlp_encode
from .scorer import TokenScorer
from .db import log_trade

class TradeExecutor:
    def __init__(self, wallet):
        self.wallet = wallet
        self.token_scorer = TokenScorer(config.get("target_tokens", []))

    def sign_tx(self, tx, private_key_hex):
        try:
            private_key_bytes = bytes.fromhex(private_key_hex.replace('0x', ''))
            sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)

            unsigned_tx = [
                tx['nonce'],
                tx['gasPrice'],
                tx['gas'],
                bytes.fromhex(tx['to'].replace('0x', '')),
                tx['value'],
                tx['data'],
                tx['chainId'],
                0,
                0
            ]
            rlp_unsigned = rlp_encode(unsigned_tx)
            tx_hash = sha3_256(rlp_unsigned).digest()

            signature = sk.sign_digest(tx_hash, sigencode=lambda r, s, order: r.to_bytes(32, 'big') + s.to_bytes(32, 'big'))
            r = int.from_bytes(signature[:32], 'big')
            s = int.from_bytes(signature[32:], 'big')
            v = tx['chainId'] * 2 + 35 + (1 if s % 2 != 0 else 0)

            signed_tx = [
                tx['nonce'],
                tx['gasPrice'],
                tx['gas'],
                bytes.fromhex(tx['to'].replace('0x', '')),
                tx['value'],
                tx['data'],
                v,
                r,
                s
            ]
            raw_tx = rlp_encode(signed_tx)
            return '0x' + raw_tx.hex()
        except Exception as e:
            logging.error(f"[SIGN ERROR] {e}")
            return None

    def send_tx(self, signed_tx_hex):
        try:
            payload = {
                "jsonrpc": "2.0",
                "method": "eth_sendRawTransaction",
                "params": [signed_tx_hex],
                "id": 1
            }
            req = urllib.request.Request(config['rpc_url'], json.dumps(payload).encode(), {'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=10) as res:
                result = json.loads(res.read())
                return result.get('result')
        except Exception as e:
            logging.error(f"[SEND TX ERROR] {e}")
            return None

    def execute_trade(self, adaptive_volume, action_type):
        try:
            eth_balance = get_eth_balance(config['wallet_address'])
            gas_price = int(Decimal(get_gas_price()) * Decimal('1.02'))
            gas_cost_eth = Decimal(gas_price * config['gas_limit']) / Decimal('1e18')
            available_balance = eth_balance - gas_cost_eth

            if available_balance <= Decimal('0.001'):
                logging.warning(f"[NO FUNDS] {eth_balance:.6f} ETH too low after gas.")
                return

            price = now_price()
            if price == 0:
                logging.warning("[PRICE ZERO] Abort trade.")
                return

            trade_eth = min(Decimal(str(config['trade_volume'])) * adaptive_volume, available_balance)
            if trade_eth <= Decimal('0.001'):
                logging.warning(f"[SKIP] Final trade {trade_eth:.6f} ETH too small.")
                return

            value_wei = int(trade_eth * Decimal('1e18'))
            nonce = get_nonce(config['wallet_address'])
            token_out = self.token_scorer.best_token()

            deadline = int(time.time()) + 600
            data = encode_swap_exact_eth_for_tokens(
                min_tokens_out=config['min_tokens_out'],
                path=[config['weth_address'], token_out],
                to=config['wallet_address'],
                deadline=deadline
            )

            tx = {
                "nonce": nonce,
                "gasPrice": gas_price,
                "gas": config['gas_limit'],
                "to": config['uniswap_router'],
                "value": value_wei,
                "data": data,
                "chainId": 1
            }

            signed = self.sign_tx(tx, config['private_key'])
            if signed:
                if config.get('simulate', False):
                    logging.info(f"[SIMULATE] SWAP {trade_eth:.6f} ETH → {token_out[:8]}...")
                    return
                tx_hash = self.send_tx(signed)
                if tx_hash:
                    logging.info(f"[SWAP SUCCESS] TX {tx_hash[:10]}...")
                    log_trade(
                        time.strftime('%Y-%m-%d %H:%M:%S'),
                        "SWAP",
                        tx_hash,
                        float(price),
                        float(trade_eth)
                    )
        except Exception as e:
            logging.error(f"[EXECUTE TRADE ERROR] {e}")
