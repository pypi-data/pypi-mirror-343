import json
import urllib.request
import logging
from decimal import Decimal
from hashlib import sha3_256

_config = None  # Private module-level config

def set_config(c):
    global _config
    _config = c

def require_config():
    if _config is None:
        raise RuntimeError("Config not set. Call set_config(config) first.")

def safe_rpc(method, params):
    require_config()
    try:
        payload = json.dumps({
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }).encode()
        req = urllib.request.Request(
            _config['rpc_url'],
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
    require_config()
    try:
        data = safe_rpc("eth_call", [{
            "to": _config["price_feed_address"],
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
        logging.error(f"[GAS PRICE ERROR] {e}")
        return 0

def get_nonce(address):
    try:
        nonce = safe_rpc('eth_getTransactionCount', [address, 'latest'])
        return int(nonce, 16) if nonce else 0
    except Exception as e:
        logging.error(f"[NONCE ERROR] {e}")
        return 0

def eth_to_tokens(min_tokens_out, path, to, deadline):
    """Encode calldata for swapExactETHForTokens"""
    try:
        method = '7ff36ab5'
        a = hex(min_tokens_out)[2:].rjust(64, '0')
        b = hex(len(path))[2:].rjust(64, '0')
        p = ''.join(x.lower().replace('0x', '').rjust(64, '0') for x in path)
        t = to.lower().replace('0x', '').rjust(64, '0')
        d = hex(deadline)[2:].rjust(64, '0')
        return bytes.fromhex(method + a + b + p + t + d)
    except Exception as e:
        logging.error(f"[ENCODE ETH->TOKENS ERROR] {e}")
        return b''

def tokens_to_eth(amount_in, amount_out_min, path, to, deadline):
    """Encode calldata for swapExactTokensForETH"""
    try:
        method = '18cbafe5'
        a_in = hex(amount_in)[2:].rjust(64, '0')
        a_out = hex(amount_out_min)[2:].rjust(64, '0')
        p_count = hex(len(path))[2:].rjust(64, '0')
        p = ''.join(x.lower().replace('0x', '').rjust(64, '0') for x in path)
        t = to.lower().replace('0x', '').rjust(64, '0')
        d = hex(deadline)[2:].rjust(64, '0')
        return bytes.fromhex(method + a_in + a_out + p_count + p + t + d)
    except Exception as e:
        logging.error(f"[ENCODE TOKENS->ETH ERROR] {e}")
        return b''
