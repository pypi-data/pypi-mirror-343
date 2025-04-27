from math import radians, cos, sin, asin, sqrt

def haversine_distance(lat1, lon1, lat2, lon2):
    """
        Calculate the great circle distance between two points on the Earth (in meters).

        This function uses the Haversine formula to calculate the shortest distance between
        two points (latitude and longitude) on the Earth's surface, accounting for the Earth's
        curvature.

        Parameters:
        lat1 (float): Latitude of the first point (in decimal degrees).
        lon1 (float): Longitude of the first point (in decimal degrees).
        lat2 (float): Latitude of the second point (in decimal degrees).
        lon2 (float): Longitude of the second point (in decimal degrees).

        Returns:
        float: The great circle distance between the two points in meters.
    """

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371000  # Radius of earth in meters
    return c * r

def is_inside_geofence(user_lat, user_lon, center_lat, center_lon, radius_meters):
    """
    Check if the given coordinates are within a geofence radius.

    This function calculates the distance between a user's location and a geofence center
    and checks whether the user is within the specified radius.

    Parameters:
    user_lat (float): Latitude of the user's location (in decimal degrees).
    user_lon (float): Longitude of the user's location (in decimal degrees).
    center_lat (float): Latitude of the geofence center (in decimal degrees).
    center_lon (float): Longitude of the geofence center (in decimal degrees).
    radius_meters (float): The radius of the geofence in meters.

    Returns:
    bool: True if the user is within the geofence radius, False otherwise.
    """
    distance = haversine_distance(user_lat, user_lon, center_lat, center_lon)
    return distance <= radius_meters
