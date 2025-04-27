import logging
import time
import random
from decimal import Decimal, InvalidOperation
from collections import deque
from .utils import safe_rpc

class TokenScorer:
    def __init__(self, tokens, min_volatility_threshold=Decimal('0.001'), rolling_window=1):
        """
        tokens: List of token addresses
        min_volatility_threshold: Minimum % movement to consider
        rolling_window: How many prices to keep per token for smoothing (1 = only last)
        """
        self.tokens = tokens
        self.min_volatility_threshold = Decimal(min_volatility_threshold)
        self.rolling_window = rolling_window
        self.last_prices = {token: deque(maxlen=rolling_window) for token in tokens}

    def safe_fetch_price(self, token_address):
        retries = 3
        delay = 2
        for attempt in range(retries):
            try:
                response = safe_rpc("eth_call", [{
                    "to": token_address,
                    "data": "0xfeaf968c"
                }, "latest"])

                if response and len(response) >= 194:
                    price_raw = int(response[130:194], 16)
                    price = Decimal(price_raw) / Decimal('1e8')
                    if price > 0:
                        return price
                    else:
                        raise ValueError("Zero price parsed.")
                else:
                    raise ValueError("Malformed eth_call response.")
            except (Exception, InvalidOperation) as e:
                logging.error(f"[PRICE FETCH RETRY {attempt+1}] {token_address} | {e}")
                time.sleep(delay + random.uniform(0, 1))
                delay *= 2

        logging.error(f"[PRICE FETCH FAILURE] {token_address} Max retries exceeded.")
        return Decimal('0')

    def score_tokens(self):
        """Score tokens based on smoothed volatility over the rolling window."""
        scored_tokens = []
        for token in self.tokens:
            try:
                current_price = self.safe_fetch_price(token)
                if current_price <= 0:
                    logging.warning(f"[SKIP TOKEN] {token} fetch resulted in zero or invalid price.")
                    continue

                price_history = self.last_prices.setdefault(token, deque(maxlen=self.rolling_window))
                if price_history:
                    previous_price = price_history[-1]
                    if previous_price > 0:
                        volatility = abs(current_price - previous_price) / previous_price
                    else:
                        volatility = Decimal('0')

                    if volatility >= self.min_volatility_threshold:
                        scored_tokens.append((token, volatility))
                        logging.info(f"[TOKEN SCORING] {token} volatility={volatility:.6f}")

                price_history.append(current_price)

            except Exception as e:
                logging.error(f"[SCORING ERROR] {token} | {e}")

        scored_tokens.sort(key=lambda x: x[1], reverse=True)
        return scored_tokens

    def best_token(self):
        """Return the single highest volatility token."""
        try:
            scored = self.score_tokens()
            if scored:
                best_token, best_score = scored[0]
                logging.info(f"[BEST TOKEN SELECTED] {best_token} | Volatility {best_score:.6f}")
                return best_token
            else:
                logging.warning("[NO HIGH VOLATILITY TOKEN FOUND] Falling back to first available token.")
                return self.tokens[0] if self.tokens else None
        except Exception as e:
            logging.error(f"[BEST TOKEN ERROR] {e}")
            return self.tokens[0] if self.tokens else None

    def top_n_tokens(self, n=3):
        """Return top N volatility-ranked tokens."""
        try:
            scored = self.score_tokens()
            top_tokens = [token for token, _ in scored[:n]]
            logging.info(f"[TOP {n} TOKENS SELECTED] {top_tokens}")
            return top_tokens
        except Exception as e:
            logging.error(f"[TOP N TOKENS ERROR] {e}")
            return []