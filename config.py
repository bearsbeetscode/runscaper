from pathlib import Path


# Paths
STRAVA_DIR = Path(__file__).parent / "gpx_files"
OUTPUT_IMAGE = Path(__file__).parent / "output_image" / "running_heatmap.png"
STATS_FILE = Path(__file__).parent / "stats_folder" / "run_stats.txt"
# Colors
BG_COLOR = "#1E1E2E"
TXT_COLOR = "#CDD6F4"
RECENT_COLOR = "#F5C2E7"
PREVIOUS_COLOR = "#CBA6F7"
HISTORY_COLOR = "#7F849C"


# Location, put coordinates that will be in the middle of wallpaper.
try:
    import my_secrets

    HOME_LAT = my_secrets.HOME_LAT
    HOME_LON = my_secrets.HOME_LON
except ImportError:
    # Fallback coordinates
    HOME_LAT = 37.82926344244314
    HOME_LON = -92.10512707843111
