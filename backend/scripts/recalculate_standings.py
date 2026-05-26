from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.database import AsyncSessionLocal
from app.jobs.recalculators.standings_recalculator import StandingsRecalculator


async def run(args: argparse.Namespace) -> dict[str, int]:
    async with AsyncSessionLocal() as session:
        recalculator = StandingsRecalculator(session)
        return await recalculator.recalculate_tournament(
            league_name=args.league,
            country=args.country,
            season_name=args.season,
            tournament_name=args.tournament,
            include_knockout=args.include_knockout,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recalculate standings from finished matches."
    )
    parser.add_argument("--league", default="Primera Division de Venezuela")
    parser.add_argument("--country", default="Venezuela")
    parser.add_argument("--season", default="2026")
    parser.add_argument("--tournament", default="Apertura")
    parser.add_argument(
        "--include-knockout",
        action="store_true",
        help="Also recalculate knockout phases. Disabled by default.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = asyncio.run(run(args))
    print("Standings recalculation completed:")
    for key, count in summary.items():
        print(f"  {key}: {count}")


if __name__ == "__main__":
    main()
