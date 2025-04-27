"""
Quant-GridBot

====================================
Quant-Grade Dynamic Ethereum Grid & Portfolio Balancing Bot
====================================

Description:
------------
Quant-GridBot is a modular, production-grade Ethereum trading system 
designed for intelligent dynamic grid trading and portfolio rebalancing 
based on live volatility and liquidity conditions. 
It interacts directly with Ethereum nodes (RPC) and performs fully signed, 
gas-optimized Uniswap transactions without relying on external heavy libraries.

Key Features:
-------------
- **Dynamic Adaptive Clustered Grid Strategy** (live volatility detection)
- **Real-Time Dual-Grid Recenter** based on market clustering
- **Portfolio Rebalancer**: Live ETH/Token ratio maintenance
- **Direct Ethereum TX Building, RLP Signing, and Broadcasting** (No `web3.py`)
- **Intelligent Token Selection** based on real-time volatility scoring
- **Persistent SQLite Trade Logging** (thread-safe)
- **Fully Modular and Extensible Codebase**
- **CLI Launchable** with `quantgridbot`
- **Supports Simulation Mode** (`simulate=True`) and Real Trading Mode
- **Graceful Shutdown** (SIGINT/SIGTERM Safe)

Exposed Modules:
-----------------
- `MasterController` (core): Boots wallet, executor, bots
- `GridBot` (grid): Adaptive ETH price grid trading with clustering
- `RebalanceBot` (rebalance): Live portfolio monitoring and corrective rebalancing
- `TradeExecutor` (executor): Transaction builder, signer, and submitter
- `DynamicWallet` (wallet): Real-time portfolio tracking
- `TokenScorer` (scorer): Token volatility analyzer
- `utils`: Ethereum RPC tools, signing helpers, encoding
- `TradeDatabase` (db): SQLite trade persistence

Configuration:
---------------
Requires a `config.json` in the root or execution directory.

Important fields:
    - `rpc_url`: Ethereum RPC endpoint URL
    - `wallet_address`: Your Ethereum wallet public address
    - `private_key`: Private key (hex, NEVER expose)
    - `simulate`: (bool) True for dry-run, False for live trading
    - `trade_volume`: Amount of ETH to trade per grid hit
    - `slippage_pct`: Maximum allowed slippage for executions
    - `grid_lower_pct`, `grid_upper_pct`: Grid width bounds
    - `grid_size`: Number of grid levels
    - `trade_cooldown`: Seconds between allowed trades
    - `refresh_interval`: Seconds between price checks
    - `target_tokens`: ERC20 token addresses for scoring/rebalancing
    - `stablecoin_address`: Stablecoin address for ETH->Stable swaps
    - `min_tokens_out`: Minimum output tolerance for swaps

Entry Point:
------------
- `AppRunner` (runner.py) — initializes entire system
- Launch with: `$ quantgridbot`

Version:
--------
- 1.1.3

Author:
-------
- LoQiseaking69
- Contact: REEL0112359.13@proton.me
"""

__version__ = "1.1.1"
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
    encode_swap_exact_eth_for_tokens
)