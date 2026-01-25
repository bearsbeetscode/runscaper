from pathlib import Path


# Paths
STRAVA_DIR = Path.home() / "Documents/GPXFiles"
OUTPUT_IMAGE = Path.home() / "Pictures/runscaper/running_heatmap.png"

# Colors
BG_COLOR = "#2E3440"
TXT_COLOR = "#ECEFF4"
DAY_COLOR = "#88C0D0"
NIGHT_COLOR = "#B48EAD"

try:
    import my_secrets

    HOME_LAT = my_secrets.HOME_LAT
    HOME_LON = my_secrets.HOME_LON
except ImportError:
    HOME_LAT = 37.82926344244314
    HOME_LON = -92.10512707843111
