from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.style import Style
from rich.text import Text
from typing import Dict, Optional

console = Console()


class AgentProgress:
    """Manages progress tracking for multiple agents."""

    def __init__(self) -> None:
        self.agent_status: Dict[str, Dict[str, Optional[str]]] = {}
        self.table = Table(show_header=False, box=None, padding=(0, 1))
        self.live = Live(self.table, console=console, refresh_per_second=4)
        self.started = False

    def start(self) -> None:
        """Start the progress display."""
        if not self.started:
            self.live.start()
            self.started = True

    def stop(self) -> None:
        """Stop the progress display."""
        if self.started:
            self.live.stop()
            self.started = False

    def update_status(
        self, agent_name: str, ticker: Optional[str] = None, status: str = ""
    ) -> None:
        """Update the status of an agent."""
        if agent_name not in self.agent_status:
            self.agent_status[agent_name] = {"status": "", "ticker": None}

        if ticker:
            self.agent_status[agent_name]["ticker"] = ticker
        if status:
            self.agent_status[agent_name]["status"] = status

        self._refresh_display()

    def _refresh_display(self) -> None:
        """Refresh the progress display."""
        self.table.columns.clear()
        self.table.add_column(width=100)

        # Sort agents with Risk Management and Portfolio Management at the bottom
        def sort_key(item):
            agent_name = item[0]
            if "risk_management" in agent_name:
                return (2, agent_name)
            elif "portfolio_management" in agent_name:
                return (3, agent_name)
            else:
                return (1, agent_name)

        for agent_name, info in sorted(self.agent_status.items(), key=sort_key):
            status = info["status"]
            ticker = info["ticker"]

            # Create the status text with appropriate styling
            # Handle None status by defaulting to empty string for comparison and display
            current_status = status if status is not None else ""

            if current_status.lower() == "done":
                style = Style(color="green", bold=True)
                symbol = "✓"
            elif current_status.lower() == "error":
                style = Style(color="red", bold=True)
                symbol = "✗"
            else:
                style = Style(color="yellow")
                symbol = "⋯"

            agent_display = agent_name.replace("_agent", "").replace("_", " ").title()
            status_text = Text()
            status_text.append(f"{symbol} ", style=style)
            status_text.append(f"{agent_display:<20}", style=Style(bold=True))

            if ticker:
                status_text.append(f"[{ticker}] ", style=Style(color="cyan"))
            status_text.append(current_status, style=style)

            self.table.add_row(status_text)


# Create a global instance
progress = AgentProgress()
