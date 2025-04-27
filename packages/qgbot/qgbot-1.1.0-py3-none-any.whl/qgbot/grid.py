import time
import logging
import numpy as np
from decimal import Decimal
from collections import deque
from threading import Event
from .utils import now_price

class GridBot:
    def __init__(self, wallet, executor, config):
        self.wallet = wallet
        self.executor = executor
        self.config = config
        self.grid_size = config['grid_size']
        self.base_cooldown = config['trade_cooldown']
        self.refresh_interval = config['refresh_interval']
        self.price_history = deque(maxlen=120)
        self._stop_event = Event()

        self.mode = "single"
        self.primary_grid = []
        self.secondary_grid = []
        self.primary_center = Decimal('0')
        self.secondary_center = Decimal('0')
        self.last_trade_time = 0
        self.last_recenter = time.monotonic()

    def stop(self):
        self._stop_event.set()

    def setup_single_grid(self, center_price):
        self.primary_center = center_price
        lower = Decimal('1') - Decimal(str(self.config['grid_lower_pct'])) / Decimal('2')
        upper = Decimal('1') + Decimal(str(self.config['grid_upper_pct'])) / Decimal('2')
        self.primary_grid = [center_price * Decimal(str(x)) for x in np.linspace(float(lower), float(upper), self.grid_size + 1)]
        self.secondary_grid = []
        logging.info(f"[SINGLE GRID] Setup around ${center_price:.2f}")

    def setup_dual_grids(self, center1, center2):
        lower1 = Decimal('1') - Decimal(str(self.config['grid_lower_pct'])) / Decimal('2')
        upper1 = Decimal('1') + Decimal(str(self.config['grid_upper_pct'])) / Decimal('2')
        self.primary_grid = [center1 * Decimal(str(x)) for x in np.linspace(float(lower1), float(upper1), (self.grid_size // 2) + 1)]

        lower2 = Decimal('1') - Decimal(str(self.config['grid_lower_pct'])) / Decimal('2')
        upper2 = Decimal('1') + Decimal(str(self.config['grid_upper_pct'])) / Decimal('2')
        self.secondary_grid = [center2 * Decimal(str(x)) for x in np.linspace(float(lower2), float(upper2), (self.grid_size // 2) + 1)]

        self.primary_center = center1
        self.secondary_center = center2

        logging.info(f"[DUAL GRID] Centers ${center1:.2f} and ${center2:.2f}")

    def detect_clusters(self):
        try:
            prices = np.array(self.price_history)
            if len(prices) < 30:
                return None

            hist, edges = np.histogram(prices, bins=5)
            peaks = np.argsort(hist)[-2:]  # Take two largest bins

            centers = []
            for idx in peaks:
                low = Decimal(str(edges[idx]))
                high = Decimal(str(edges[idx + 1]))
                centers.append((low + high) / 2)

            if abs(centers[0] - centers[1]) / min(centers) > Decimal('0.02'):  # Only if 2% apart
                logging.info(f"[CLUSTERS DETECTED] {centers[0]:.2f} and {centers[1]:.2f}")
                return sorted(centers)
            else:
                return None
        except Exception as e:
            logging.error(f"[CLUSTER DETECTION ERROR] {e}")
            return None

    def recenter(self, price):
        clusters = self.detect_clusters()
        if clusters:
            self.mode = "dual"
            self.setup_dual_grids(clusters[0], clusters[1])
        else:
            self.mode = "single"
            self.setup_single_grid(price)
        self.last_recenter = time.monotonic()

    def check_grids(self, price):
        now_ts = time.monotonic()
        self.price_history.append(price)

        if now_ts - self.last_recenter > 180 or not self.primary_grid:
            self.recenter(price)

        if now_ts - self.last_trade_time < self.base_cooldown:
            return

        grids_to_check = self.primary_grid if self.mode == "single" else self.primary_grid + self.secondary_grid
        centers = [self.primary_center] if self.mode == "single" else [self.primary_center, self.secondary_center]

        for center, grid in zip(centers, [self.primary_grid, self.secondary_grid] if self.mode == "dual" else [self.primary_grid]):
            for level in grid:
                spread = (price - level) / center
                if abs(spread) <= Decimal(str(self.config['slippage_pct'])):
                    logging.info(f"[GRID HIT] {self.mode.upper()} Mode | SWAP at spread {spread:.6f}")
                    self.executor.execute_trade(adaptive_volume=Decimal('1.0'))
                    self.last_trade_time = now_ts
                    return

    def run(self):
        logging.info("[GRIDBOT] Running (Dynamic Cluster Mode)...")
        while not self._stop_event.is_set():
            try:
                price = now_price()
                if price > 0:
                    self.check_grids(price)
                else:
                    logging.warning("[ZERO PRICE] Waiting...")
                time.sleep(self.refresh_interval)
            except Exception as e:
                logging.error(f"[GRIDBOT RUNTIME ERROR] {e}")
                time.sleep(5)