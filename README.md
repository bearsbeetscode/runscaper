# RunScaper

A minimalist Python tool that transforms your Strava GPX history into a high-resolution heatmap wallpaper. It highlights your progress by color-coding your most recent activities and generates a summary for desktop widgets.

---

## Features

- **Heatmap Generation:** Processes `.gpx` files to create a clean PNG visualization.
- **Activity Layering:** Uses z-ordering to place recent runs on top of historical data for better visibility.
- **Dynamic Styling:** Differentiates between your latest run, previous run, and older history using custom color themes.
- **Stats Export:** Writes total distance, peak elevation, and last run date to a text file for use in desktop widget.

---

## Setup

### 1. Install Dependencies

Ensure you have Python installed, then install the required libraries:

```bash
pip install -r requirements.txt
```
