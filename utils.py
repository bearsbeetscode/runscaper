from datetime import datetime
import gpxpy


def get_coordinates(gpx_file):
    """
    Returns:
        tuple: (list of lat/lon points, total distance in km,
            activity type string, list of elavations, start time)
    """
    with open(gpx_file, "r") as f:
        gpx = gpxpy.parse(f)

    points = []
    elevations = []
    is_night = False
    start_time = None

    try:
        # Check if the run was a "night" run based on start hour (19:00 - 06:00)
        first_point_time = gpx.tracks[0].segments[0].points[0].time
        if first_point_time is not None:
            start_time = first_point_time
        if isinstance(first_point_time, datetime):
            if first_point_time.hour >= 19 or first_point_time.hour < 6:
                is_night = True
    except (IndexError, AttributeError):
        pass

    # Extracts track points and elevation
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append((point.latitude, point.longitude))
                elevations.append(point.elevation if point.elevation is not None else 0)

    run_distance_km = gpx.length_2d() / 1000
    activity_type = "night" if is_night else "day"
    return points, run_distance_km, activity_type, elevations, start_time
