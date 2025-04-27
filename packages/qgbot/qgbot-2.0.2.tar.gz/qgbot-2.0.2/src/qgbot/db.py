import sqlite3
import threading
import logging
import time
from datetime import datetime

class TradeDatabase:
    def __init__(self, db_path='trades.db'):
        self.db_path = db_path
        self._lock = threading.RLock()
        self._connect()

    def _connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False, timeout=10)
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
            logging.info(f"[DB] Connected successfully to {self.db_path}")
        except Exception as e:
            logging.critical(f"[DB CONNECT ERROR] {e}")
            raise SystemExit(1)

    def log_trade(self, action, tx_hash, eth_price, eth_amount, timestamp=None):
        """Log a trade entry safely."""
        retries = 3
        delay = 2
        for attempt in range(retries):
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
                    logging.info(f"[DB] Trade logged: {action.upper()} | {eth_amount:.6f} ETH @ ${eth_price:.2f}")
                return
            except sqlite3.OperationalError as e:
                logging.error(f"[DB LOCK ERROR] Retry {attempt+1} | {e}")
                time.sleep(delay + random.uniform(0, 1))
                delay *= 2
            except Exception as e:
                logging.error(f"[DB LOG TRADE ERROR] {e}")
                break

        logging.critical(f"[DB] Failed to log trade after retries.")

    def fetch_all_trades(self):
        """Fetch all trades ordered by newest first."""
        try:
            with self._lock:
                self.cur.execute("SELECT * FROM trades ORDER BY id DESC")
                trades = self.cur.fetchall()
                logging.info(f"[DB] Fetched {len(trades)} trades.")
                return trades
        except Exception as e:
            logging.error(f"[DB FETCH ERROR] {e}")
            return []

    def backup_db(self, backup_path='trades_backup.db'):
        """Backup the current database to a specified file."""
        try:
            with self._lock:
                dest_conn = sqlite3.connect(backup_path)
                self.conn.backup(dest_conn)
                dest_conn.close()
                logging.info(f"[DB] Backup completed to {backup_path}")
        except Exception as e:
            logging.error(f"[DB BACKUP ERROR] {e}")

    def close(self):
        """Close the database connection safely."""
        try:
            with self._lock:
                self.conn.close()
                logging.info("[DB] Connection closed.")
        except Exception as e:
            logging.error(f"[DB CLOSE ERROR] {e}")

# === Singleton Export ===
trade_db = TradeDatabase()

def log_trade(action, tx_hash, eth_price, eth_amount, timestamp=None):
    """External log function for legacy style compatibility."""
    trade_db.log_trade(action, tx_hash, eth_price, eth_amount, timestamp)