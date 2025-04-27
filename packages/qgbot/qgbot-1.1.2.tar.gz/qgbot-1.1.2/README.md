# Quant-GridBot

**Modular Quant-Grade Intelligent Volatility-Aware ETH-to-Token Grid Trading Bot**

---
![img](https://github.com/LoQiseaking69/qgbot/blob/main/Qgbot.PNG)
___

## Features
- Real Ethereum RPC Trading (No Web3.py dependency)
- Adaptive Dynamic Grid Trading Strategy
- Volatility-Weighted Grid Level Adjustment (tightens/widens based on live volatility)
- Intelligent Token Selection Based on Real-Time Volatility Scoring
- Real Ethereum Transaction Signing (ECDSA/RLP Encoding)
- Real SQLite Trade Logging (Persistent Local Database)
- Fully Modular Code Architecture (Core, Grid, Rebalance, Executor, Wallet, Scorer, DB, Utils)
- CLI Launchable via `quantgridbot`
- Supports Simulation Mode (Dry Run) and Live Trading Mode
- Graceful Shutdown and Signal Handling
- BSD 3-Clause Licensed (Open Source)

---

## Installation

Clone the repository and install locally:

```bash
git clone https://github.com/LoQiseaking69/qgbot.git
cd qgbot
pip install .
```

---

## Configuration

Before running, create a `config.json` file at the project root.

**Required fields include:**
- `rpc_url`: Your Ethereum RPC endpoint (Infura, Alchemy, custom node)
- `wallet_address`: Your Ethereum wallet address
- `private_key`: Private key for signing transactions (**keep secret**)
- `simulate`: `true` for dry-run, `false` for real transactions
- `trade_volume`: Amount of ETH per trade
- `grid_lower_pct`, `grid_upper_pct`: Grid boundaries relative to ETH price
- `grid_size`: Number of grid levels
- `target_tokens`: List of ERC20 token contract addresses
- `slippage_pct`, `trade_cooldown`, `refresh_interval`: Trade controls

An example template `config.example.json` is provided.

---

## Usage

After configuring:

```bash
quantgridbot
```

The bot will start monitoring live ETH prices, dynamically adjusting the grid, selecting the best tokens, and executing trades based on grid levels.

---

## Project Structure

- `src/qgbot/core.py` — System controller (launches GridBot and RebalanceBot)
- `src/qgbot/grid.py` — Grid trading logic and execution
- `src/qgbot/rebalance.py` — Portfolio balance monitoring
- `src/qgbot/executor.py` — Trade building, signing, and Uniswap execution
- `src/qgbot/wallet.py` — Live ETH balance fetching and valuation
- `src/qgbot/scorer.py` — Token volatility scoring and best selection
- `src/qgbot/utils.py` — Ethereum RPC communication and RLP helpers
- `src/qgbot/db.py` — Thread-safe TradeDatabase (SQLite logger)
## License
___

BSD 3-Clause License.  
See the [LICENSE](LICENSE) file for full license text.
