"""
Quant-GridBot

============================================
Quant-Grade Dynamic Ethereum Grid Trading & Intelligent Portfolio Management Engine
============================================

Description:
------------
Quant-GridBot is a modular, production-grade Ethereum trading system 
engineered for real-time volatility-based grid trading and intelligent asset rebalancing.
It interacts directly with Ethereum nodes (RPC) and performs gas-optimized 
Uniswap transactions using native transaction construction and RLP signing 
without relying on heavy external libraries.

Key Features:
-------------
- **Dynamic Adaptive Grid Strategy** (live volatility-clustered trading)
- **Dual-Cluster Volatility Recenter** (adaptive spread widening/narrowing)
- **Live Portfolio Rebalancer** (real-time ETH/Token ratio management)
- **Direct Ethereum Transaction Building and RLP Signing** (no `web3.py` dependency)
- **Live Token Volatility Scoring Engine** (automatic best token detection)
- **Full Thread-Safe SQLite Trade Logging**
- **Automated Gas Estimation and Retry Protection** (for gas/price/nonce fetches)
- **Interactive CLI and Live Rich Dashboard** (thread monitoring, portfolio updates)
- **Simulation Mode (`simulate=True`)** and **Production Trading Mode**
- **Graceful Safe Shutdown** (full SIGINT/SIGTERM capture and recovery)
- **Backup-Ready Database and Configurable Trade Parameters**
- **Heartbeat Thread Monitoring and Auto-Restart Mechanism**

Primary Exposed Modules:
-------------------------
- `MasterController` (core) — Oversees wallet, bots, trading threads, and health checks
- `GridBot` (grid) — Dynamic Ethereum grid trading engine
- `RebalanceBot` (rebalance) — Live ETH/token balancing strategy executor
- `TradeExecutor` (executor) — Transaction builder, signer, sender
- `DynamicWallet` (wallet) — Live ETH/token balance fetcher and tracker
- `TokenScorer` (scorer) — Token volatility ranking and dynamic selection
- `TradeDatabase` (db) — Trade history persistence (SQLite3)
- `utils` — Core Ethereum RPC, RLP signing, and encoding helper utilities

Configuration Overview:
------------------------
Requires a `config.json` in the project directory with fields like:
    - `rpc_url` : Ethereum RPC Endpoint
    - `secondary_rpc_url` : Optional backup RPC node
    - `wallet_address` : Wallet public address
    - `private_key` : Private key for signing (Hex format)
    - `simulate` : True/False for dry-run mode
    - `trade_volume` : Base ETH amount per trade
    - `grid_lower_pct`, `grid_upper_pct` : Grid spread bounds
    - `grid_size` : Number of grid levels
    - `trade_cooldown` : Minimum seconds between trades
    - `slippage_pct` : Max tolerated slippage on swap
    - `refresh_interval` : GridBot refresh interval (seconds)
    - `rebalance_threshold` : Rebalance deviation threshold
    - `target_tokens` : ERC20 token addresses for volatility scoring
    - `stablecoin_address` : Stablecoin for rebalancing trades
    - `min_tokens_out` : Swap protection minimum

Launch Entry Point:
-------------------
- `AppRunner` (main.py) — Bootstraps the full Quant-GridBot system.
- Launch with: `$ quantgridbot`

Version:
--------
- 2.1.3

Author:
-------
- LoQiseaking69
- Contact: REEL0112359.13@proton.me
"""

__version__ = "2.1.3"
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
    eth_to_tokens, tokens_to_eth, fetch_token_price_via_uniswap
)