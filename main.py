import gpxpy
import matplotlib.pyplot as plt
from pathlib import Path

STRAVA_DIR = Path.home() / "Documents/GPXFiles"
OUTPUT_IMAGE = Path.home() / "Pictures/runscaper/running_heatmap.png"
BG_COLOR = "#2E3440"
LINE_COLOR = "#88C0D0"


def get_coordinates(gpx_file):
    with open(gpx_file, "r") as f:
        gpx = gpxpy.parse(f)

    points = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append((point.latitude, point.longitude))
    return points


def plot_heatmap(all_runs):
    plt.figure(figsize=(16, 9), facecolor=BG_COLOR)
    ax = plt.gca()
    ax.set_facecolor(BG_COLOR)

    for run in all_runs:
        lats, lons = zip(*run)
        plt.plot(lons, lats, color=LINE_COLOR, alpha=0.3, linewidth=1.5)

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
    all_runs = [get_coordinates(f) for f in gpx_files]
    plot_heatmap(all_runs)
    print(f"Heatmap saved to {OUTPUT_IMAGE}")


if __name__ == "__main__":
    main()
