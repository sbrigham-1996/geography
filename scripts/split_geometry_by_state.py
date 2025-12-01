#!/usr/bin/env python3
"""
Split the nationwide TIGER county shapefile into one GeoJSON
per state folder.

Input
-----
data/geo/tl_2023_us_county/tl_2023_us_county.shp
states/<State>/counties.csv  (only for mapping state names)

Output
------
states/<State>/counties.geojson   (ESRI:4326 / WGS84)
"""

from pathlib import Path
import geopandas as gpd
import pandas as pd
from tqdm import tqdm

ROOT      = Path(__file__).resolve().parent.parent
STATE_DIR = ROOT / "states"
COUNTY_SHP = ROOT / "scripts/data/geo/tl_2023_us_county/tl_2023_us_county.shp"

# --------------------------------------------------------------------
print("Loading nationwide county geometry …")
gdf_all = gpd.read_file(COUNTY_SHP).to_crs(4326)     # WGS84 / Leaflet

# Keep only fields we want to preserve
gdf_all = gdf_all[["STATEFP", "GEOID", "NAME", "geometry"]]

# Optional: cross-walk state FIPS → state name via your CSVs
print("Building state FIPS → name map …")
fips_to_name = {}
for state_folder in STATE_DIR.iterdir():
    csv_path = state_folder / "counties.csv"
    if not csv_path.exists():
        continue
    df = pd.read_csv(csv_path, dtype=str, usecols=["state_fips"])
    fips_to_name[df.at[0, "state_fips"]] = state_folder.name

# --------------------------------------------------------------------
for state_fips, state_name in tqdm(sorted(fips_to_name.items()), desc="states"):
    folder = STATE_DIR / state_name
    out_geojson = folder / "counties.geojson"
    if out_geojson.exists():
        print(f"[skip] {state_name:20} geojson already exists")
        continue

    gdf_state = gdf_all[gdf_all["STATEFP"] == state_fips]
    if gdf_state.empty:
        print(f"[warn] {state_name:20} no matching geometries")
        continue

    gdf_state.to_file(out_geojson, driver="GeoJSON")
    print(f"✓ {state_name:20} → counties.geojson ({len(gdf_state)} features)")

print("Done.")