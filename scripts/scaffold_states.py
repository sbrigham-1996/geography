#!/usr/bin/env python3
"""
scaffold_states.py  •  Run once to set up a states/ directory tree.
"""
from pathlib import Path
import json
import csv

# 50 U.S. states in Title Case
STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming",
]

BASE = Path(__file__).parent
state_root = BASE / "states"
state_root.mkdir(exist_ok=True)

for state in STATES:
    folder = state_root / state
    folder.mkdir(exist_ok=True)

    # 1) info.json – minimal placeholder
    info_file = folder / "info.json"
    if not info_file.exists():
        with info_file.open("w") as fp:
            json.dump(
                {
                    "state": state,
                    "capital": "",
                    "population": None,
                    "area_sq_mi": None,
                    "fips": "",
                },
                fp,
                indent=2,
            )

    # 2) cities.csv – header row only
    cities_file = folder / "cities.csv"
    if not cities_file.exists():
        with cities_file.open("w", newline="") as fp:
            writer = csv.writer(fp)
            writer.writerow(["city", "latitude", "longitude", "population"])

    # 3) counties.csv – header row only
    counties_file = folder / "counties.csv"
    if not counties_file.exists():
        with counties_file.open("w", newline="") as fp:
            writer = csv.writer(fp)
            writer.writerow(["county", "fips", "seat", "population"])

print("✅  Scaffold complete: 50 state folders with stub files.")