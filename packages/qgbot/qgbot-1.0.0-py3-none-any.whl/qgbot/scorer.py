import logging
from decimal import Decimal
from .utils import safe_rpc

class TokenScorer:
    def __init__(self, tokens, min_volatility_threshold=Decimal('0.001')):
        self.tokens = tokens
        self.last_prices = {token: Decimal('0') for token in tokens}
        self.min_volatility_threshold = min_volatility_threshold

    def fetch_price(self, token):
        try:
            data = safe_rpc("eth_call", [{
                "to": token,
                "data": "0xfeaf968c"
            }, "latest"])
            if data and len(data) >= 194:
                price = Decimal(int(data[130:194], 16)) / Decimal('1e8')
                return price if price > 0 else Decimal('0')
        except Exception as e:
            logging.warning(f"[TOKEN PRICE FETCH ERROR] Token: {token} | {e}")
        return Decimal('0')

    def score_tokens(self):
        scored = []
        for token in self.tokens:
            try:
                price_now = self.fetch_price(token)
                price_last = self.last_prices.get(token, Decimal('0'))

                if price_now > 0 and price_last > 0:
                    volatility = abs(price_now - price_last) / price_last
                else:
                    volatility = Decimal('0')

                # Only consider if volatility meets threshold
                if volatility >= self.min_volatility_threshold:
                    scored.append((token, volatility))

                if price_now > 0:
                    self.last_prices[token] = price_now

            except Exception as e:
                logging.error(f"[SCORING ERROR] Token: {token} | {e}")

        # Sort tokens by volatility descending
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    def best_token(self):
        scored = self.score_tokens()
        if scored:
            best = scored[0][0]
            logging.info(f"[BEST TOKEN SELECTED] {best} (Volatility {scored[0][1]:.6f})")
            return best
        else:
            logging.warning("[NO GOOD TOKEN] Fallback to first configured token.")
            return self.tokens[0] if self.tokens else None
