import json
import urllib.request
import logging
from decimal import Decimal
from hashlib import sha3_256

# Config will be passed explicitly where needed, no hidden global dependency
config = None

def set_config(c):
    global config
    config = c

def safe_rpc(method, params):
    if config is None:
        raise RuntimeError("Config not set. Call set_config(config) first.")
    try:
        payload = json.dumps({
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }).encode()
        req = urllib.request.Request(
            config['rpc_url'],
            payload,
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=10) as res:
            result = json.loads(res.read())
            return result.get('result')
    except Exception as e:
        logging.error(f"[RPC ERROR] {method}: {e}")
        return None

def keccak(data):
    return sha3_256(data).digest()

def rlp_encode(item):
    if isinstance(item, int):
        if item == 0:
            return b'\x80'
        item_bytes = item.to_bytes((item.bit_length() + 7) // 8, 'big')
        return rlp_encode(item_bytes)
    elif isinstance(item, bytes):
        if len(item) == 1 and item[0] < 0x80:
            return item
        if len(item) <= 55:
            return bytes([0x80 + len(item)]) + item
        else:
            length_bytes = len(item).to_bytes((len(item).bit_length() + 7) // 8, 'big')
            return bytes([0xb7 + len(length_bytes)]) + length_bytes + item
    elif isinstance(item, list):
        output = b''.join(rlp_encode(x) for x in item)
        if len(output) <= 55:
            return bytes([0xc0 + len(output)]) + output
        else:
            length_bytes = len(output).to_bytes((len(output).bit_length() + 7) // 8, 'big')
            return bytes([0xf7 + len(length_bytes)]) + length_bytes + output
    else:
        raise TypeError(f"Unsupported RLP type: {type(item)}")

def now_price():
    if config is None:
        raise RuntimeError("Config not set. Call set_config(config) first.")
    try:
        data = safe_rpc("eth_call", [{
            "to": config["price_feed_address"],
            "data": "0xfeaf968c"
        }, "latest"])
        if data and len(data) >= 194:
            price = Decimal(int(data[130:194], 16)) / Decimal('1e8')
            return price if price > 0 else Decimal('0')
    except Exception as e:
        logging.error(f"[PRICE ERROR] {e}")
    return Decimal('0')

def get_eth_balance(address):
    try:
        balance = safe_rpc("eth_getBalance", [address, "latest"])
        return Decimal(int(balance, 16)) / Decimal('1e18') if balance else Decimal('0')
    except Exception as e:
        logging.error(f"[BALANCE ERROR] {e}")
        return Decimal('0')

def get_gas_price():
    try:
        gas = safe_rpc('eth_gasPrice', [])
        return int(gas, 16) if gas else 0
    except Exception as e:
        logging.error(f"[GAS ERROR] {e}")
        return 0

def get_nonce(address):
    try:
        nonce = safe_rpc('eth_getTransactionCount', [address, 'latest'])
        return int(nonce, 16) if nonce else 0
    except Exception as e:
        logging.error(f"[NONCE ERROR] {e}")
        return 0

def encode_swap_exact_eth_for_tokens(min_tokens_out, path, to, deadline):
    try:
        method_id = '7ff36ab5'
        min_tokens_hex = hex(min_tokens_out)[2:].rjust(64, '0')
        path_count = hex(len(path))[2:].rjust(64, '0')
        path_encoded = ''.join(addr.lower().replace('0x', '').rjust(64, '0') for addr in path)
        to_encoded = to.lower().replace('0x', '').rjust(64, '0')
        deadline_encoded = hex(deadline)[2:].rjust(64, '0')
        full_data = method_id + min_tokens_hex + path_count + path_encoded + to_encoded + deadline_encoded
        return bytes.fromhex(full_data)
    except Exception as e:
        logging.error(f"[ENCODE SWAP ERROR] {e}")
        return b''
