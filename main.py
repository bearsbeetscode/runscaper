import gpxpy
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib import patheffects

STRAVA_DIR = Path.home() / "Documents/GPXFiles"
OUTPUT_IMAGE = Path.home() / "Pictures/runscaper/running_heatmap.png"
BG_COLOR = "#2E3440"
GLOW_COLOR = "#88C0D0"
LINE_COLOR = "#E0F2F7"
TXT_COLOR = "#ECEFF4"


def get_coordinates(gpx_file):
    with open(gpx_file, "r") as f:
        gpx = gpxpy.parse(f)

    points = []
    run_distance_meters = gpx.length_2d()

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append((point.latitude, point.longitude))
    run_distance_km = run_distance_meters / 1000
    return points, run_distance_km


def plot_heatmap(all_runs, total_km):
    plt.figure(figsize=(16, 9), facecolor=BG_COLOR)
    ax = plt.gca()
    ax.set_facecolor(BG_COLOR)

    for run in all_runs:
        lats, lons = zip(*run)
        plt.plot(lons, lats, color=GLOW_COLOR, alpha=0.1, linewidth=4, zorder=1)
        plt.plot(lons, lats, color=LINE_COLOR, alpha=0.6, linewidth=1, zorder=2)

    stats_text = f"Total Distance: {total_km:.1f} km"
    txt = plt.text(
        0.95,
        0.05,
        stats_text,
        transform=ax.transAxes,
        color=TXT_COLOR,
        fontsize=20,
        fontweight="bold",
        ha="right",
        family="monospace",
    )
    txt.set_path_effects([patheffects.withStroke(linewidth=3, foreground=BG_COLOR)])

    plt.gca().set_aspect("equal", adjustable="datalim")
    plt.axis("off")
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0.02)

    output_path = OUTPUT_IMAGE
    plt.savefig(
        output_path, facecolor=BG_COLOR, dpi=160, bbox_inches="tight", pad_inches=0
    )
    return output_path


def main():
    gpx_files = list(STRAVA_DIR.glob("*.gpx"))

    all_runs = []
    grand_total_km = 0.0

    for f in gpx_files:
        coords, dist = get_coordinates(f)
        if len(coords) > 2:
            all_runs.append(coords)
            grand_total_km += dist

    if all_runs:
        plot_heatmap(all_runs, grand_total_km)
        print(f"Heatmap saved to {OUTPUT_IMAGE}")


if __name__ == "__main__":
    main()
