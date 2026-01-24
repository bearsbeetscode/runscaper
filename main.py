import matplotlib.pyplot as plt
from matplotlib import patheffects
import config
import utils


def plot_heatmap(activity_data, total_km):
    plt.figure(figsize=(16, 9), facecolor=config.BG_COLOR)
    ax = plt.gca()
    ax.set_facecolor(config.BG_COLOR)

    all_lats, all_lons = [], []
    highest_alt = 0

    for points, act_type, elevations in activity_data:
        if not points:
            continue
        lats, lons = zip(*points)
        all_lats.extend(lats)
        all_lons.extend(lons)
        highest_alt = max(highest_alt, max(elevations))

        color = config.NIGHT_COLOR if act_type == "night" else config.DAY_COLOR

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

    if all_lats:
        max_dist = max(
            max(abs(lat - config.HOME_LAT) for lat in all_lats),
            max(abs(lon - config.HOME_LON) for lon in all_lons),
        )
        padding = max_dist * 1.1
        ax.set_ylim(config.HOME_LAT - padding, config.HOME_LAT + padding)
        ax.set_xlim(config.HOME_LON - padding, config.HOME_LON + padding)
    stats_text = f"Total Distance: {total_km:.1f} km.\nPeak: {highest_alt:.0f} m"
    txt = plt.text(
        0.95,
        0.05,
        stats_text,
        transform=ax.transAxes,
        color=config.TXT_COLOR,
        fontsize=20,
        fontweight="bold",
        ha="right",
        family="monospace",
    )
    txt.set_path_effects(
        [patheffects.withStroke(linewidth=3, foreground=config.BG_COLOR)]
    )

    plt.gca().set_aspect("equal", adjustable="datalim")
    plt.axis("off")
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0.02)

    output_path = config.OUTPUT_IMAGE
    plt.savefig(
        output_path,
        facecolor=config.BG_COLOR,
        dpi=160,
        bbox_inches="tight",
        pad_inches=0,
    )
    return output_path


def main():
    gpx_files = list(config.STRAVA_DIR.glob("*.gpx"))

    activity_data = []
    grand_total_km = 0.0

    for f in gpx_files:
        coords, dist, act_type, elevs = utils.get_coordinates(f)
        if len(coords) > 2:
            activity_data.append((coords, act_type, elevs))
            grand_total_km += dist

    if activity_data:
        plot_heatmap(activity_data, grand_total_km)
        print(f"Heatmap saved to {config.OUTPUT_IMAGE}")


if __name__ == "__main__":
    main()
