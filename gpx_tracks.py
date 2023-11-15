import gpxpy
import gpxpy.gpx
from geopy.distance import geodesic


def filter_gpx_by_radius(gpx_data, center_lat, center_lon, radius_km):
    """
    Filter GPX track points to those within a specified radius from a center point.

    :param gpx_data: GPX file data as a string.
    :param center_lat: Latitude of the center point.
    :param center_lon: Longitude of the center point.
    :param radius_km: Radius in kilometers.
    :return: Filtered GPX data as a string.
    """
    gpx = gpxpy.parse(gpx_data)
    center = (center_lat, center_lon)

    for track in gpx.tracks:
        for segment in track.segments:
            segment.points = [point for point in segment.points if
                              geodesic((point.latitude, point.longitude), center).km <= radius_km]

    return gpx.to_xml()


def filter_gpx_by_time(gpx_data, start_time, end_time):
    """
    Filter GPX track points to those within a specified time range.

    :param gpx_data: GPX file data as a string.
    :param start_time: Start time as a datetime object.
    :param end_time: End time as a datetime object.
    :return: Filtered GPX data as a string.
    """
    gpx = gpxpy.parse(gpx_data)

    for track in gpx.tracks:
        for segment in track.segments:
            segment.points = [point for point in segment.points if
                              start_time <= point.time.replace(tzinfo=None) <= end_time]

    return gpx.to_xml()

def filter_gpx_by_time_and_radius(gpx_data, start_time, end_time, center_lat, center_lon, radius_km):
    """
    Filter GPX track points to those within a specified time range and radius from a center point.

    :param gpx_data: GPX file data as a string.
    :param start_time: Start time as a datetime object.
    :param end_time: End time as a datetime object.
    :param center_lat: Latitude of the center point.
    :param center_lon: Longitude of the center point.
    :param radius_km: Radius in kilometers.
    :return: Filtered GPX data as a string.
    """
    gpx = gpxpy.parse(gpx_data)
    center = (center_lat, center_lon)

    for track in gpx.tracks:
        for segment in track.segments:
            segment.points = [point for point in segment.points if
                              start_time <= point.time.replace(tzinfo=None) <= end_time and
                              geodesic((point.latitude, point.longitude), center).km <= radius_km]

    return gpx.to_xml()


