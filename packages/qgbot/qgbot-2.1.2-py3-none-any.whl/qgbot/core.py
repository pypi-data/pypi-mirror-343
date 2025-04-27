import threading
import logging
import json
import time
import os
import psutil
from pathlib import Path
from decimal import Decimal
from typing import Dict, Any

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich import box
from rich.traceback import install as install_rich_traceback

from .utils import set_config
from .wallet import DynamicWallet
from .executor import TradeExecutor
from .grid import GridBot
from .rebalance import RebalanceBot

console = Console()
install_rich_traceback()

class ThreadMeta:
    def __init__(self, thread: threading.Thread) -> None:
        self.thread = thread
        self.restart_count = 0
        self.last_restart_time = time.strftime("%H:%M:%S")
        self.psutil_proc = psutil.Process(os.getpid())

class MasterController:
    def __init__(self, config_path: str = 'config.json') -> None:
        self.config_path: str = config_path
        self.config: Dict[str, Any] = self._load_config()
        set_config(self.config)

        self.wallet: DynamicWallet = self._build_wallet()
        self.executor: TradeExecutor = self._build_executor()
        self.gridbot: GridBot = self._build_gridbot()
        self.rebalancer: RebalanceBot = self._build_rebalancer()
        self._threads_meta: Dict[str, ThreadMeta] = {}
        self._running: threading.Event = threading.Event()

    def _load_config(self) -> Dict[str, Any]:
        config_file = Path(self.config_path)
        if not config_file.is_file():
            logging.critical(f"[CONFIG ERROR] File not found: {self.config_path}")
            raise SystemExit(1)
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            logging.info(f"[CONFIG] Loaded successfully from {self.config_path}")
            return config
        except (json.JSONDecodeError, Exception) as e:
            logging.critical(f"[CONFIG ERROR] {e}")
            raise SystemExit(1)

    def _build_wallet(self) -> DynamicWallet:
        try:
            wallet = DynamicWallet(self.config)
            logging.info("[MASTER] Wallet initialized.")
            return wallet
        except Exception as e:
            logging.critical(f"[WALLET INIT ERROR] {e}")
            raise SystemExit(1)

    def _build_executor(self) -> TradeExecutor:
        return TradeExecutor(self.wallet, self.config)

    def _build_gridbot(self) -> GridBot:
        return GridBot(self.wallet, self.executor, self.config)

    def _build_rebalancer(self) -> RebalanceBot:
        return RebalanceBot(self.wallet, self.executor, self.config)

    def _show_launch_message(self) -> None:
        title = Text("QGBOT", style="bold magenta on black", justify="center")
        subtitle = Text("Quant-Grade Intelligent ETH Grid Trading Engine", style="cyan", justify="center")
        version = Text("Version 2.0.0", style="bold green", justify="center")

        body = Panel.fit(
            Text.from_markup(
                "[bold cyan]Initializing core modules...[/bold cyan]\n"
                "[bold yellow]Loading wallet and RPC interface...[/bold yellow]\n"
                "[bold green]Preparing dynamic grid strategy...[/bold green]\n"
                "[bold magenta]Activating rebalancer systems...[/bold magenta]\n"
                "[bold white]Monitoring network and liquidity pools...[/bold white]"
            ),
            title="[bold magenta]Qgbot Launch[/bold magenta]",
            border_style="bright_magenta"
        )

        console.rule(title)
        console.print(subtitle)
        console.print(version)
        console.print(body)
        console.rule(style="bright_magenta")

    def _start_grid_thread(self) -> None:
        thread = threading.Thread(target=self.gridbot.run, name="GridBotThread", daemon=True)
        thread.start()
        self._threads_meta["GridBotThread"] = ThreadMeta(thread)

    def _start_rebalance_thread(self) -> None:
        thread = threading.Thread(target=self.rebalancer.run, name="RebalanceBotThread", daemon=True)
        thread.start()
        self._threads_meta["RebalanceBotThread"] = ThreadMeta(thread)

    def start_all(self) -> None:
        if self._running.is_set():
            logging.warning("[MASTER] Start requested but already running.")
            return

        self._running.set()
        self._threads_meta.clear()

        try:
            self._show_launch_message()
            self._start_grid_thread()
            self._start_rebalance_thread()
            logging.info("[MASTER] All bots started successfully.")
        except Exception as e:
            logging.error(f"[MASTER START ERROR] {e}")
            self.stop_all()

    def stop_all(self) -> None:
        if not self._running.is_set():
            logging.warning("[MASTER] Stop requested but already stopped.")
            return

        logging.info("[MASTER] Initiating shutdown sequence...")
        self._running.clear()

        try:
            self.gridbot.stop()
            self.rebalancer.stop()

            for meta in self._threads_meta.values():
                if meta.thread.is_alive():
                    meta.thread.join(timeout=10)
                    if meta.thread.is_alive():
                        logging.warning(f"[MASTER] Thread {meta.thread.name} did not shut down cleanly.")

            logging.info("[MASTER] Shutdown complete.")
        except Exception as e:
            logging.error(f"[MASTER STOP ERROR] {e}")

    def show_portfolio(self) -> None:
        try:
            portfolio = self.wallet.fetch_live_tokens()
            total_usd = Decimal('0')

            table = Table(title="Wallet Portfolio", style="bold cyan")
            table.add_column("Token", justify="center", style="bold green")
            table.add_column("Balance", justify="right", style="bold yellow")
            table.add_column("USD Value", justify="right", style="bold magenta")

            for symbol, data in portfolio.items():
                balance = data.get('balance', Decimal('0'))
                usd_value = data.get('usd_value', Decimal('0'))
                total_usd += usd_value
                table.add_row(
                    symbol,
                    f"{balance:.6f}",
                    f"${usd_value:.2f}"
                )

            table.add_row("─" * 10, "─" * 10, "─" * 10)
            table.add_row(
                "[bold white]TOTAL[/bold white]",
                "",
                f"[bold green]${total_usd:.2f}[/bold green]"
            )

            console.print(table)

        except Exception as e:
            logging.error(f"[PORTFOLIO ERROR] {e}")

    def _render_status_table(self) -> Table:
        table = Table(title="Bot Thread Monitor", box=box.ROUNDED, style="bold blue")
        table.add_column("Thread Name", style="cyan", justify="center")
        table.add_column("Alive", style="green", justify="center")
        table.add_column("Restarts", style="magenta", justify="center")
        table.add_column("Last Restart", style="yellow", justify="center")
        table.add_column("CPU%", style="bright_green", justify="center")
        table.add_column("Mem%", style="bright_blue", justify="center")

        for name, meta in self._threads_meta.items():
            alive = "✅" if meta.thread.is_alive() else "❌"
            cpu = f"{meta.psutil_proc.cpu_percent() / psutil.cpu_count():.2f}%"
            mem = f"{meta.psutil_proc.memory_percent():.2f}%"
            table.add_row(
                name,
                alive,
                str(meta.restart_count),
                meta.last_restart_time,
                cpu,
                mem
            )

        return table

    def _heartbeat_check(self) -> None:
        for name, meta in list(self._threads_meta.items()):
            if not meta.thread.is_alive():
                logging.error(f"[HEARTBEAT] {name} died. Restarting...")
                if "GridBot" in name:
                    self._start_grid_thread()
                elif "RebalanceBot" in name:
                    self._start_rebalance_thread()

                meta.restart_count += 1
                meta.last_restart_time = time.strftime("%H:%M:%S")

    def run_forever(self) -> None:
        try:
            self.start_all()
            logging.info("[MASTER] Running indefinitely. Press CTRL+C to terminate.")

            last_portfolio_update = time.time()
            last_monitor_check = time.time()
            update_interval = 300
            monitor_interval = 5

            with Live(self._render_status_table(), refresh_per_second=1, console=console) as live:
                while self._running.is_set():
                    time.sleep(1)

                    if time.time() - last_portfolio_update >= update_interval:
                        self.show_portfolio()
                        last_portfolio_update = time.time()

                    if time.time() - last_monitor_check >= monitor_interval:
                        live.update(self._render_status_table())
                        self._heartbeat_check()
                        last_monitor_check = time.time()

        except KeyboardInterrupt:
            logging.warning("[MASTER] KeyboardInterrupt received. Stopping all...")
            self.stop_all()
        except Exception as e:
            logging.error(f"[MASTER RUN ERROR] {e}")
            self.stop_all()