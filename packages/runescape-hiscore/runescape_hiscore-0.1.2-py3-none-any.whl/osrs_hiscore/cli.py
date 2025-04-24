# src/osrs_hiscore/cli.py

import sys
import argparse
import json
import csv
from rich.console import Console
from rich.table import Table
from rich import box
from .core import fetch_stats, xp_for_level, make_sparkline


def main():
    p = argparse.ArgumentParser(description="Fetch OSRS OldSchool hiscores")
    p.add_argument("username", help="Your OldSchool username")
    p.add_argument("--json", metavar="FILE", help="Write stats as JSON")
    p.add_argument("--csv",  metavar="FILE", help="Write stats as CSV")
    args = p.parse_args()

    console = Console()
    try:
        mode, stats = fetch_stats(args.username)
    except Exception as e:
        console.print(f"[bold red]Error:[/] {e}")
        sys.exit(1)

    # Enrich stats with XP‐gaps
    for s in stats:
        lvl, xp = s["level"], s["xp"]
        s["to_next"] = max(0, xp_for_level(lvl+1) - xp) if lvl < 99 else 0
        s["to_200m"] = max(0, 200_000_000 - xp)

    # JSON export
    if args.json:
        with open(args.json, "w") as f:
            json.dump(stats, f, indent=2)
        console.print(f"[green]Wrote JSON to {args.json}[/]")
        return

    # CSV export
    if args.csv:
        with open(args.csv, "w", newline="") as f:
            w = csv.DictWriter(
                f, fieldnames=["skill", "rank", "level", "xp", "to_next", "to_200m"])
            w.writeheader()
            w.writerows(stats)
        console.print(f"[green]Wrote CSV to {args.csv}[/]")
        return

    # Pretty‐print table
    console.rule(f"[bold yellow]Hiscores for {args.username} ({mode})[/]")
    console.print(
        f"XP distribution: {make_sparkline([s['xp'] for s in stats])}\n")

    table = Table(box=box.SIMPLE_HEAVY)
    table.add_column("Skill", style="cyan", no_wrap=True)
    table.add_column("Lvl", style="magenta", justify="right")
    table.add_column("XP", style="green", justify="right")
    table.add_column("To Next", style="yellow", justify="right")
    table.add_column("To 200M", style="yellow", justify="right")
    table.add_column("Rank", style="white", justify="right")

    for s in stats:
        table.add_row(
            s["skill"],
            str(s["level"]),
            f"{s['xp']:,}",
            f"{s['to_next']:,}" if s["to_next"] else "—",
            f"{s['to_200m']:,}" if s["to_200m"] else "—",
            f"{s['rank']:,}"
        )

    console.print(table)
