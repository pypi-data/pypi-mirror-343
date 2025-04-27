import time
import logging
import numpy as np
from decimal import Decimal
from collections import deque
from .utils import now_price

class GridBot:
    def __init__(self, wallet, executor):
        self.wallet = wallet
        self.executor = executor
        self.grid_size = config['grid_size']
        self.base_cooldown = config['trade_cooldown']
        self.refresh_interval = config['refresh_interval']
        self.grid = []
        self.center_price = Decimal('0')
        self.last_trade_time = 0
        self.last_grid_update = time.monotonic()
        self.price_history = deque(maxlen=30)
        self.cooldown_dynamic = self.base_cooldown

    def setup_grid(self, center_price, volatility_scale=1.0):
        self.center_price = center_price
        self.grid = []
        lower = Decimal('1') - (Decimal(str(config['grid_lower_pct'])) * Decimal('0.5') * Decimal(volatility_scale))
        upper = Decimal('1') + (Decimal(str(config['grid_upper_pct'])) * Decimal('0.5') * Decimal(volatility_scale))
        for s in np.linspace(float(lower), float(upper), self.grid_size + 1):
            self.grid.append(center_price * Decimal(str(s)))
        logging.info(f"[GRID SETUP] {len(self.grid)} Levels (Volatility Scale {volatility_scale})")

    def estimate_volatility(self):
        try:
            if len(self.price_history) < 5:
                return Decimal('1.0')
            prices = np.array(self.price_history)
            vol = np.std(np.diff(prices) / prices[:-1])
            return Decimal('1.5') if vol > 0.015 else Decimal('0.7') if vol < 0.003 else Decimal('1.0')
        except Exception as e:
            logging.warning(f"[VOLATILITY ERROR] {e}")
            return Decimal('1.0')

    def dynamic_cooldown(self):
        scale = self.estimate_volatility()
        return self.base_cooldown * 2 if scale > Decimal('1.2') else max(2, self.base_cooldown // 2) if scale < Decimal('0.8') else self.base_cooldown

    def check_grid(self, price):
        now_ts = time.monotonic()
        self.price_history.append(price)

        if now_ts - self.last_grid_update > 300:
            self.setup_grid(price, volatility_scale=self.estimate_volatility())
            self.last_grid_update = now_ts
            return

        if now_ts - self.last_trade_time < self.cooldown_dynamic:
            return

        for level in self.grid:
            spread = (price - level) / self.center_price
            if abs(spread) <= Decimal(str(config['slippage_pct'])):
                action_type = "SWAP"
                logging.info(f"[GRID HIT] {action_type} at spread {round(spread,6)}")
                self.executor.execute_trade(Decimal('1.0'), action_type)
                self.last_trade_time = now_ts
                self.cooldown_dynamic = self.dynamic_cooldown()
                break

    def run(self):
        while not stop_event.is_set():
            try:
                price = now_price()
                if price > 0:
                    self.check_grid(price)
                else:
                    logging.warning("[ZERO PRICE]")
                time.sleep(self.refresh_interval)
            except Exception as e:
                logging.error(f"[GRIDBOT ERROR] {e}")
                time.sleep(5)
