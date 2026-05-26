from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.database import AsyncSessionLocal
from app.jobs.importers.structure_importer import StructureImporter


DEFAULT_SEED_PATH = BACKEND_ROOT / "data" / "seeds" / "futve_2026_apertura_structure.json"


async def run(seed_path: Path) -> dict[str, int]:
    async with AsyncSessionLocal() as session:
        importer = StructureImporter(session)
        return await importer.import_file(seed_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Seed structural FUTVE data into the database."
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=DEFAULT_SEED_PATH,
        help=f"Seed JSON path. Defaults to {DEFAULT_SEED_PATH}",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = asyncio.run(run(args.file))
    print("Seed completed:")
    for key, count in summary.items():
        print(f"  {key}: {count} created")


if __name__ == "__main__":
    main()
