import time
import logging
import random
import numpy as np
from decimal import Decimal, InvalidOperation
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
        self.last_recenter_time = time.monotonic()
        self.last_price = Decimal('0')

    def stop(self):
        self._stop_event.set()

    def safe_now_price(self):
        retries = 3
        delay = 2
        for attempt in range(retries):
            if self._stop_event.is_set():
                return Decimal('0')
            try:
                price = Decimal(now_price())
                if price <= 0:
                    raise ValueError("Zero or negative price fetched.")
                return price
            except (Exception, InvalidOperation) as e:
                logging.error(f"[SAFE PRICE RETRY {attempt+1}] {e}")
                time.sleep(delay + random.uniform(0, 1))
                delay *= 2
        logging.error("[SAFE PRICE ERROR] Max retries exceeded.")
        return Decimal('0')

    def setup_single_grid(self, center_price):
        try:
            self.primary_center = center_price
            pct = Decimal(str(self.config.get('grid_lower_pct', '0.02'))) / Decimal('2')
            lower = Decimal('1') - pct
            upper = Decimal('1') + pct
            self.primary_grid = [center_price * Decimal(str(x)) for x in np.linspace(float(lower), float(upper), self.grid_size + 1)]
            self.secondary_grid = []
            logging.info(f"[SINGLE GRID] Centered at ${center_price:.2f} | Grid Levels: {len(self.primary_grid)}")
        except Exception as e:
            logging.error(f"[SETUP SINGLE GRID ERROR] {e}")

    def setup_dual_grids(self, center1, center2):
        try:
            pct = Decimal(str(self.config.get('grid_lower_pct', '0.02'))) / Decimal('2')
            lower = Decimal('1') - pct
            upper = Decimal('1') + pct

            half_size = (self.grid_size // 2) + 1
            self.primary_grid = [center1 * Decimal(str(x)) for x in np.linspace(float(lower), float(upper), half_size)]
            self.secondary_grid = [center2 * Decimal(str(x)) for x in np.linspace(float(lower), float(upper), half_size)]

            self.primary_center = center1
            self.secondary_center = center2

            logging.info(f"[DUAL GRID] Primary ${center1:.2f} | Secondary ${center2:.2f} | Levels per grid: {len(self.primary_grid)}")
        except Exception as e:
            logging.error(f"[SETUP DUAL GRID ERROR] {e}")
            
    def detect_clusters(self):
        try:
            prices = np.array(self.price_history)
            if len(prices) < 30:
                logging.debug("[CLUSTER DETECTION] Not enough data points yet.")
                return None

            hist, edges = np.histogram(prices, bins=5)
            peak_indices = np.argsort(hist)[-2:]

            centers = []
            for idx in peak_indices:
                low = Decimal(str(edges[idx]))
                high = Decimal(str(edges[idx + 1]))
                centers.append((low + high) / 2)

            if len(centers) >= 2:
                spread = abs(centers[0] - centers[1]) / min(centers)
                if spread > Decimal('0.02'):
                    logging.info(f"[CLUSTERS DETECTED] Centers: {centers[0]:.2f}, {centers[1]:.2f} | Spread: {spread:.4f}")
                    return sorted(centers)
                else:
                    logging.debug(f"[CLUSTERS TOO CLOSE] Centers: {centers[0]:.2f} & {centers[1]:.2f} | Spread too small: {spread:.4f}")
            return None
        except Exception as e:
            logging.error(f"[CLUSTER DETECTION ERROR] {e}")
            return None

    def recenter_grids(self, price):
        if self._stop_event.is_set():
            return
        try:
            clusters = self.detect_clusters()
            if clusters:
                self.mode = "dual"
                self.setup_dual_grids(clusters[0], clusters[1])
            else:
                self.mode = "single"
                self.setup_single_grid(price)
            self.last_recenter_time = time.monotonic()
        except Exception as e:
            logging.error(f"[RECENTER GRID ERROR] {e}")

    def check_grids(self, price):
        if self._stop_event.is_set():
            return

        try:
            now_ts = time.monotonic()
            self.price_history.append(price)

            if now_ts - self.last_recenter_time > self.config.get('recenter_interval', 180) or not self.primary_grid:
                self.recenter_grids(price)

            if now_ts - self.last_trade_time < self.base_cooldown:
                return

            grids_to_check = self.primary_grid if self.mode == "single" else self.primary_grid + self.secondary_grid
            centers = [self.primary_center] if self.mode == "single" else [self.primary_center, self.secondary_center]

            for center, grid in zip(centers, [self.primary_grid, self.secondary_grid] if self.mode == "dual" else [self.primary_grid]):
                for level in grid:
                    spread = (price - level) / center
                    if abs(spread) <= Decimal(str(self.config.get('slippage_pct', '0.005'))):
                        logging.info(f"[GRID HIT] Mode={self.mode.upper()} | Price={price:.2f} | Level={level:.2f} | Spread={spread:.6f}")
                        self.executor.execute_trade(adaptive_volume=Decimal('1.0'))
                        self.last_trade_time = now_ts
                        return
        except Exception as e:
            logging.error(f"[CHECK GRIDS ERROR] {e}")
            
    def run(self):
        logging.info("[GRIDBOT] Starting Dynamic Grid Execution...")
        while not self._stop_event.is_set():
            try:
                price = self.safe_now_price()
                if price > 0:
                    self.last_price = price
                    self.check_grids(price)
                else:
                    logging.warning("[INVALID PRICE] Skipping cycle...")
                time.sleep(self.refresh_interval)
            except Exception as e:
                logging.error(f"[GRIDBOT RUN ERROR] {e}")
                time.sleep(5)

        logging.info("[GRIDBOT] Stop signal received. GridBot halted cleanly.")