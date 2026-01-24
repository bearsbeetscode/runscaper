from datetime import datetime
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
DAY_COLOR = "#88C0D0"
NIGHT_COLOR = "#B48EAD"


def get_coordinates(gpx_file):
    with open(gpx_file, "r") as f:
        gpx = gpxpy.parse(f)

    points = []
    is_night = False

    try:
        first_point_time = gpx.tracks[0].segments[0].points[0].time
        if first_point_time and hasattr(first_point_time, "hour"):
            if first_point_time.hour >= 19 or first_point_time.hour < 6:
                is_night = True
    except (IndexError, AttributeError):
        pass

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append((point.latitude, point.longitude))
    run_distance_km = gpx.length_2d() / 1000
    activity_type = "night" if is_night else "day"
    return points, run_distance_km, activity_type


def plot_heatmap(activity_data, total_km):
    plt.figure(figsize=(16, 9), facecolor=BG_COLOR)
    ax = plt.gca()
    ax.set_facecolor(BG_COLOR)

    for points, act_type in activity_data:
        if not points:
            continue
        lats, lons = zip(*points)

        color = NIGHT_COLOR if act_type == "night" else DAY_COLOR
        plt.plot(lons, lats, color=color, alpha=0.05, linewidth=8, zorder=1)
        plt.plot(lons, lats, color=color, alpha=0.2, linewidth=3, zorder=2)
        plt.plot(
            lons,
            lats,
            color=color,
            alpha=0.8,
            linewidth=0.6,
            zorder=3,
            solid_joinstyle="round",
        )
    stats_text = f"Total Distance: {total_km:.1f} km."
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

    activity_data: list[tuple] = []
    grand_total_km = 0.0

    for f in gpx_files:
        coords, dist, act_type = get_coordinates(f)
        if len(coords) > 2:
            activity_data.append((coords, act_type))
            grand_total_km += dist

    if activity_data:
        plot_heatmap(activity_data, grand_total_km)
        print(f"Heatmap saved to {OUTPUT_IMAGE}")


if __name__ == "__main__":
    main()
