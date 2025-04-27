"""
Quant-GridBot

====================================
Modular Quant-Grade Intelligent Volatility-Aware ETH-to-Token Grid Trading Bot
====================================

Description:
------------
Quant-GridBot is a modular, production-grade Ethereum-based autonomous trading system
engineered for dynamic grid-based volatility exploitation with real-time adaptive controls.
It directly interacts with Ethereum RPC nodes and executes fully signed on-chain Uniswap trades.

Core Features:
--------------
- Dynamic Adaptive Grid Trading Strategy (reactive to live ETH price)
- Real-Time Volatility-Weighted Grid Adjustment
- Intelligent Best-Token Selection Based on Live Volatility Scoring
- Native Ethereum Transaction Building, Signing (ECDSA/RLP), and Broadcasting (no web3.py dependency)
- Persistent Local Trade Logging using SQLite Database
- Fully Modular, Scalable, Extensible Codebase
- CLI Launchable (`quantgridbot`)
- Supports Simulation (Dry Run) and Live Trading Modes
- Fully Asynchronous, Multi-Threaded, and Graceful Shutdown-Ready
- Real Production-Grade Signal Handling (SIGINT, SIGTERM)

Exposed Modules:
----------------
- MasterController (core): System orchestrator launching GridBot and RebalanceBot
- GridBot (grid): Live ETH price monitoring and grid-trade execution
- RebalanceBot (rebalance): Portfolio balance monitoring and health tracking
- TradeExecutor (executor): Transaction builder, signer, and Uniswap trader
- DynamicWallet (wallet): Fetches live ETH balance and USD valuation
- TokenScorer (scorer): Live scoring of ERC20 tokens based on real-time volatility
- Utility Functions (utils): Ethereum RPC handlers, RLP encoding, signing helpers
- TradeDatabase (db): Thread-safe SQLite trade logger and persistent storage handler

Configuration:
--------------
Requires a valid `config.json` at project root.
Important fields:
    - rpc_url (Ethereum RPC endpoint URL)
    - wallet_address (Your public Ethereum address)
    - private_key (For transaction signing — keep private and secured)
    - simulate (True to simulate trades, False for real trades)
    - trade_volume (ETH size per trade)
    - slippage_pct (Acceptable slippage around grid levels)
    - grid_lower_pct, grid_upper_pct (Grid width below/above center price)
    - grid_size (Number of grid levels)
    - trade_cooldown (Cooldown period between trades)
    - refresh_interval (Price refresh interval)
    - target_tokens (List of ERC20 token addresses for volatility scoring)

Entry Point:
------------
- AppRunner (runner): Initializes and controls bot lifecycle
- CLI Command: `quantgridbot`

Version:
--------
- 1.1.0

Author:
-------
- LoQiseaking69
- REEL0112359.13@proton.me
"""

__version__ = "1.1.0"
__author__ = "LoQiseaking69"
__email__ = "REEL0112359.13@proton.me"

# === Expose Core Components ===
from .core import MasterController
from .grid import GridBot
from .rebalance import RebalanceBot
from .executor import TradeExecutor
from .wallet import DynamicWallet
from .scorer import TokenScorer
from .utils import (
    safe_rpc, keccak, rlp_encode, now_price,
    get_eth_balance, get_gas_price, get_nonce,
    encode_swap_exact_eth_for_tokens
)
from .db import TradeDatabase