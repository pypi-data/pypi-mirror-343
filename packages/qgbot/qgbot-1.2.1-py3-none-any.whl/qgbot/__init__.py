"""
Quant-GridBot

============================================
Quant-Grade Dynamic Ethereum Grid & Portfolio Balancing Engine
============================================

Description:
------------
Quant-GridBot is a modular, production-grade Ethereum trading system 
engineered for dynamic volatility-based grid trading and intelligent portfolio 
rebalancing. It interacts directly with Ethereum nodes (RPC) and performs 
gas-optimized Uniswap transactions using native transaction building and RLP signing, 
without relying on heavy external libraries.

Key Features:
-------------
- **Dynamic Adaptive Clustered Grid Strategy** (real-time volatility detection)
- **Dual-Grid Volatility Recenter** (automatic dual cluster formation)
- **Live Portfolio Rebalancer** (maintains ETH/Token ratios actively)
- **Direct Ethereum Transaction Construction and RLP Signing** (no `web3.py`)
- **Token Volatility Scoring Engine** (live performance-based selection)
- **Thread-Safe Persistent SQLite Trade Logging**
- **Full Retry Protection** on Price, Gas, Nonce Fetches
- **CLI Launchable** (`quantgridbot`) and modular extensibility
- **Simulation Mode** (`simulate=True`) or Real Trading Mode
- **Graceful Safe Shutdown** (SIGINT/SIGTERM handled cleanly)
- **Backup-Capable Database Layer**

Primary Exposed Modules:
-------------------------
- `MasterController` (core) — Orchestrates wallet, executor, and bots
- `GridBot` (grid) — Dynamic Ethereum price grid trading using cluster analysis
- `RebalanceBot` (rebalance) — Live ETH/Token portfolio maintenance
- `TradeExecutor` (executor) — Gas-optimized transaction building and sending
- `DynamicWallet` (wallet) — Live ETH and token balance tracking
- `TokenScorer` (scorer) — Token scoring based on volatility momentum
- `TradeDatabase` (db) — Thread-safe SQLite trade persistence with backup hooks
- `utils` — Ethereum RPC utilities, signing, encoding, helper functions

Configuration Overview:
------------------------
Requires a `config.json` in the execution directory.

Essential fields:
    - `rpc_url` : Ethereum RPC Endpoint URL
    - `wallet_address` : Your Ethereum wallet public address
    - `private_key` : Private key (hex format — never expose)
    - `simulate` : Boolean toggle for dry-run or live trading
    - `trade_volume` : ETH amount to trade per grid hit
    - `grid_lower_pct`, `grid_upper_pct` : Grid width percentage bounds
    - `grid_size` : Number of grid levels
    - `trade_cooldown` : Minimum seconds between allowed trades
    - `slippage_pct` : Maximum tolerated slippage for executions
    - `refresh_interval` : GridBot price check interval
    - `rebalance_threshold` : Max deviation before rebalancer acts
    - `target_tokens` : ERC20 token addresses for volatility scoring
    - `stablecoin_address` : Stablecoin token for rebalancing
    - `min_tokens_out` : Minimum expected output tokens to safeguard swaps

Launch Entry Point:
-------------------
- `AppRunner` (main.py) — Bootstraps the entire trading system.
- Launch command: `$ quantgridbot`

Version:
--------
- 1.2.1

Author:
-------
- LoQiseaking69
- Contact: REEL0112359.13@proton.me
"""

__version__ = "1.2.1"
__author__ = "LoQiseaking69"
__email__ = "REEL0112359.13@proton.me"

from .core import MasterController
from .grid import GridBot
from .rebalance import RebalanceBot
from .executor import TradeExecutor
from .wallet import DynamicWallet
from .scorer import TokenScorer
from .db import TradeDatabase
from .utils import (
    safe_rpc, keccak, rlp_encode, now_price,
    get_eth_balance, get_gas_price, get_nonce,
    eth_to_tokens, tokens_to_eth
)