import gpxpy


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
