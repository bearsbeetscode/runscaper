import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import config
import utils
from datetime import datetime


def save_stats_for_widget(total_km, peak_alt, last_date):
    stats_string = f"{total_km:.1f} km {peak_alt:.0f} {last_date}"

    with open(config.STATS_FILE, "w") as f:
        f.write(stats_string)


def plot_heatmap(activity_data):
    """
    Generates PNG heatmap of activities.
    Uses z-ordering to highlight recent activities over historical ones.
    """
    plt.figure(figsize=(16, 9), facecolor=config.BG_COLOR)
    ax = plt.gca()
    ax.set_facecolor(config.BG_COLOR)

    all_lats, all_lons = [], []
    highest_alt = 0
    total_activities = len(activity_data)

    for i, (points, _, elevations) in enumerate(activity_data):
        if not points:
            continue

        lats, lons = zip(*points)
        all_lats.extend(lats)
        all_lons.extend(lons)

        current_peak = max(elevations) if elevations else 0
        highest_alt = max(highest_alt, current_peak)

        if i == total_activities - 1:  # Latest activity
            color = config.RECENT_COLOR
            alpha_main = 0.9
            z_order_base = 20
        elif i == total_activities - 2:  # Previous
            color = config.PREVIOUS_COLOR
            alpha_main = 0.7
            z_order_base = 10
        else:  # Historical
            color = config.HISTORY_COLOR
            alpha_main = 0.4
            z_order_base = 1

        # Plot "glow"/"shadow" line behind main path
        plt.plot(
            lons,
            lats,
            color=color,
            alpha=0.1,
            antialiased=True,
            linewidth=6,
            zorder=z_order_base,
        )
        # Plot main path
        plt.plot(
            lons,
            lats,
            color=color,
            alpha=alpha_main,
            linewidth=3,
            zorder=z_order_base + 1,
            solid_joinstyle="round",
        )
    # Center map around HOME_LAT/HOME_LON coordinates
    if all_lats:
        max_dist = max(
            max(abs(lat - config.HOME_LAT) for lat in all_lats),
            max(abs(lon - config.HOME_LON) for lon in all_lons),
        )
        padding = max_dist * 1.15
        ax.set_ylim(config.HOME_LAT - padding, config.HOME_LAT + padding)
        ax.set_xlim(config.HOME_LON - padding, config.HOME_LON + padding)

    plt.gca().set_aspect("equal", adjustable="datalim")
    plt.axis("off")
    plt.margins(0)

    plt.savefig(
        config.OUTPUT_IMAGE,
        facecolor=config.BG_COLOR,
        dpi=300,
        bbox_inches="tight",
        pad_inches=0,
    )
    plt.close()
    return highest_alt


def main():
    # Load GPX files from directory
    gpx_files = list(config.STRAVA_DIR.glob("*.gpx"))

    activity_data = []
    grand_total_km = 0.0

    for f in gpx_files:
        coords, dist, act_type, elevs, run_time = utils.get_coordinates(f)
        if len(coords) > 2:
            activity_data.append(
                {
                    "coords": coords,
                    "dist": dist,
                    "type": act_type,
                    "elevs": elevs,
                    "time": run_time,
                }
            )
            grand_total_km += dist

    if activity_data:
        # Sorts by time, to get latest run
        activity_data.sort(key=lambda x: x["time"] if x["time"] else datetime.min)

        plot_ready_data = [(a["coords"], a["type"], a["elevs"]) for a in activity_data]
        peak_alt = plot_heatmap(plot_ready_data)

        last_date = (
            activity_data[-1]["time"].strftime("%d %b")
            if activity_data[-1]["time"]
            else "N/A"
        )
        # Stats for display in desktop widget
        stats_string = f"󰐊 Total Distance: {grand_total_km:.2f} km\n󱓞 Total Elevation: {peak_alt:.0f} m\n󰄉 Latest Run: {last_date}"
        with open(config.STATS_FILE, "w") as f:
            f.write(stats_string)
        print(f"Success! Stats saved to {config.STATS_FILE}")


if __name__ == "__main__":
    main()
