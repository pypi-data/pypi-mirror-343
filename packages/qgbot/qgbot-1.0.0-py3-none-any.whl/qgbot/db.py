import sqlite3
import threading
import logging

class TradeDatabase:
    def __init__(self, db_path='trades.db'):
        self.db_path = db_path
        self._lock = threading.Lock()
        self._connect()

    def _connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.cur = self.conn.cursor()
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    action TEXT,
                    tx_hash TEXT,
                    eth_price REAL,
                    eth_amount REAL
                )
            """)
            self.conn.commit()
            logging.info(f"[DB] Connected to {self.db_path}")
        except Exception as e:
            logging.error(f"[DB CONNECT ERROR] {e}")
            raise

    def log_trade(self, timestamp, action, tx_hash, eth_price, eth_amount):
        try:
            with self._lock:
                self.cur.execute(
                    "INSERT INTO trades (timestamp, action, tx_hash, eth_price, eth_amount) VALUES (?, ?, ?, ?, ?)",
                    (timestamp, action, tx_hash, eth_price, eth_amount)
                )
                self.conn.commit()
                logging.info(f"[DB] Trade logged: {action} {eth_amount} @ {eth_price}")
        except Exception as e:
            logging.error(f"[DB LOG TRADE ERROR] {e}")

    def close(self):
        try:
            with self._lock:
                self.conn.close()
                logging.info("[DB] Connection closed.")
        except Exception as e:
            logging.error(f"[DB CLOSE ERROR] {e}")
