from pathlib import Path


# Paths
STRAVA_DIR = Path.home() / "Documents/GPXFiles"
OUTPUT_IMAGE = Path.home() / "Pictures/runscaper/running_heatmap.png"

# Colors
BG_COLOR = "#232136"
TXT_COLOR = "#E0DEF4"
DAY_COLOR = "#9CCFD8"
NIGHT_COLOR = "#EBBCBA"

try:
    import my_secrets

    HOME_LAT = my_secrets.HOME_LAT
    HOME_LON = my_secrets.HOME_LON
except ImportError:
    HOME_LAT = 37.82926344244314
    HOME_LON = -92.10512707843111
