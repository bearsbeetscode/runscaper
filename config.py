from pathlib import Path


# Paths
STRAVA_DIR = Path.home() / "Documents/GPXFiles"
OUTPUT_IMAGE = Path.home() / "Documents/runscaper/running_heatmap.png"
STATS_FILE = Path.home() / "Documents/runscaper/run_stats.txt"
# Colors
BG_COLOR = "#2E3440"
TXT_COLOR = "#ECEFF4"
RECENT_COLOR = "#88C0D0"
PREVIOUS_COLOR = "#81A1C1"
HISTORY_COLOR = "#4C566A"


# Location, put coordinates that will be in the middle of wallpaper.
try:
    import my_secrets

    HOME_LAT = my_secrets.HOME_LAT
    HOME_LON = my_secrets.HOME_LON
except ImportError:
    # Fallback coordinates
    HOME_LAT = 37.82926344244314
    HOME_LON = -92.10512707843111
