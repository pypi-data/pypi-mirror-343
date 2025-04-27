import sqlite3
import threading
import logging
from datetime import datetime

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
            logging.critical(f"[DB CONNECT ERROR] {e}")
            raise SystemExit(1)

    def log_trade(self, action, tx_hash, eth_price, eth_amount, timestamp=None):
        """Log a trade into the database."""
        try:
            if timestamp is None:
                timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

            with self._lock:
                self.cur.execute(
                    """
                    INSERT INTO trades (timestamp, action, tx_hash, eth_price, eth_amount)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (timestamp, action.lower(), tx_hash, float(eth_price), float(eth_amount))
                )
                self.conn.commit()
                logging.info(f"[DB] Trade logged: {action.upper()} {eth_amount} ETH @ ${eth_price}")
        except Exception as e:
            logging.error(f"[DB LOG TRADE ERROR] {e}")

    def fetch_all_trades(self):
        """Fetch all trades."""
        try:
            with self._lock:
                self.cur.execute("SELECT * FROM trades ORDER BY id DESC")
                return self.cur.fetchall()
        except Exception as e:
            logging.error(f"[DB FETCH ERROR] {e}")
            return []

    def close(self):
        """Close the database connection safely."""
        try:
            with self._lock:
                self.conn.close()
                logging.info("[DB] Connection closed.")
        except Exception as e:
            logging.error(f"[DB CLOSE ERROR] {e}")

# === Singleton export for global use ===
trade_db = TradeDatabase()

def log_trade(action, tx_hash, eth_price, eth_amount, timestamp=None):
    """Simple external log function to use like legacy `log_trade`."""
    trade_db.log_trade(action, tx_hash, eth_price, eth_amount, timestamp)