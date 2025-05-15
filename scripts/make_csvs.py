#!/usr/bin/env python3
"""
make_csvs.py
------------

Convert each states/<State>/counties.py (list of dicts called `counties`)
into a states/<State>/counties.csv that GitHub can render as a table.

Usage:
    python scripts/make_csvs.py
"""

from pathlib import Path
import importlib.util
import pandas as pd
import sys
from typing import List
import builtins
builtins.null = None        # make JSON 'null' a valid name during import

ROOT_DIR   = Path(__file__).resolve().parent.parent
STATE_DIR  = ROOT_DIR / "states"
CSV_FIELDS: List[str] | None = None     # keep original dict keys order

made, skipped, failed = 0, 0, 0

for folder in sorted(STATE_DIR.iterdir()):
    if not folder.is_dir():
        continue

    mod_path = folder / "counties.py"
    if not mod_path.exists():
        skipped += 1
        print(f"[skip] {folder.name:20} – no counties.py")
        continue

    # dynamic import of that file
    try:
        spec = importlib.util.spec_from_file_location("mod", mod_path)
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)          # type: ignore[attr-defined]
        counties = mod.counties               # type: ignore[attr-defined]
    except Exception as err:
        failed += 1
        print(f"[fail] {folder.name:20} – import error: {err}")
        continue

    # build DataFrame, preserve column order on the first loop
    if counties:
        if CSV_FIELDS is None:
            CSV_FIELDS = list(counties[0].keys())
        df = pd.DataFrame(counties)[CSV_FIELDS]
        df.to_csv(folder / "counties.csv", index=False)
        made += 1
        print(f"✓ {folder.name:20} → counties.csv ({len(df)} rows)")
    else:
        print(f"[empty] {folder.name:20} – counties list is empty")

print("\nSummary:")
print(f"  created : {made}")
print(f"  skipped : {skipped}")
print(f"  failed  : {failed}")
