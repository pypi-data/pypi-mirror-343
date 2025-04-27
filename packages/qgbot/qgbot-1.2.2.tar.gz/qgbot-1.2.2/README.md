# Quant-GridBot

**Quant-Grade Dynamic Ethereum Grid Trading and Portfolio Rebalancing Engine**

---
![img](https://github.com/LoQiseaking69/qgbot/blob/main/Qgbot.PNG)
___

## Features
- **Real Ethereum RPC Trading** (Direct transaction building — No `web3.py` dependency)
- **Adaptive Dynamic Grid Trading Strategy** (Single and Dual Grid modes with clustering)
- **Volatility Cluster Detection** (Automatic grid recentering based on live market conditions)
- **Intelligent Token Selection** (Real-time volatility scoring across multiple ERC20 tokens)
- **Real Ethereum Transaction Signing** (ECDSA + RLP encoding, gas optimization)
- **Retry-Protected Data Fetching** (Gas, nonce, balance, price retries with backoff)
- **Persistent Thread-Safe SQLite Trade Logging**
- **Fully Modular, Extensible Architecture** (Core, Grid, Rebalance, Executor, Wallet, Scorer, DB, Utils)
- **CLI Launchable** via `quantgridbot`
- **Supports Simulation Mode** (`simulate=true`) and Real Trading Mode
- **Graceful Shutdown and Signal Handling** (SIGINT/SIGTERM safe, no database corruption)
- **Production-Ready Design** (Minimal, efficient, and real-world usable)
- **BSD 3-Clause License** (Open Source)

---

## Installation

Clone the repository and install locally:

```bash
git clone https://github.com/LoQiseaking69/qgbot.git
cd qgbot
pip install .
```

Or build a wheel package using:

```bash
python -m build
pip install dist/qgbot-*.whl
```

---

## Configuration

Before running, create a `config.json` file at the project root.

**Required fields:**
- `rpc_url` : Your Ethereum RPC endpoint (e.g., Infura, Alchemy, custom node)
- `wallet_address` : Your public Ethereum address
- `private_key` : Private key for transaction signing (**keep secure**)
- `simulate` : `true` for simulation, `false` for live trading
- `trade_volume` : Amount of ETH per trade attempt
- `grid_lower_pct`, `grid_upper_pct` : Percent bounds for grid spread
- `grid_size` : Number of grid levels
- `target_tokens` : ERC20 token addresses to consider for trading
- `stablecoin_address` : Stablecoin address for ETH rebalancing
- `slippage_pct` : Maximum allowed slippage per transaction
- `trade_cooldown` : Minimum seconds between trades
- `refresh_interval` : Time between price checks and grid validations
- `rebalance_threshold` : % deviation from target ETH ratio before rebalancing triggers

> A reference example is provided as `config.example.json`.

---

## Usage

After configuring:

```bash
quantgridbot
```

The bot will:
- Monitor live Ethereum prices
- Dynamically detect price clustering
- Automatically reposition grid levels
- Select the highest-volatility token for swaps
- Execute signed Ethereum transactions
- Continuously rebalance ETH and token portfolio allocation
- Log all trades into a local persistent SQLite database.

---

## Project Structure

| Path | Description |
|:-----|:------------|
| `src/qgbot/core.py` | System controller (launches GridBot and RebalanceBot) |
| `src/qgbot/grid.py` | Dynamic volatility-aware grid trading system |
| `src/qgbot/rebalance.py` | Portfolio live ETH/token balancing bot |
| `src/qgbot/executor.py` | Ethereum transaction builder and Uniswap executor |
| `src/qgbot/wallet.py` | Wallet and portfolio live tracker |
| `src/qgbot/scorer.py` | Token volatility scoring and selection |
| `src/qgbot/db.py` | Persistent thread-safe SQLite trade database |
| `src/qgbot/utils.py` | RPC helpers, RLP encoding, signing utilities |

---

## License
___

BSD 3-Clause License.  
See the [LICENSE](LICENSE) file for full license text.

