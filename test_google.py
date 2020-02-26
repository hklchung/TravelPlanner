import googlemaps
from datetime import datetime
from secrets import gapi_key

gmaps = googlemaps.Client(key=gapi_key)

# Distance Matrix
""" Gets travel distance and time for a matrix of origins and destinations.
:param origins: One or more locations and/or latitude/longitude values,
    from which to calculate distance and time. If you pass an address as
    a string, the service will geocode the string and convert it to a
    latitude/longitude coordinate to calculate directions.
:type origins: a single location, or a list of locations, where a
    location is a string, dict, list, or tuple
:param destinations: One or more addresses and/or lat/lng values, to
    which to calculate distance and time. If you pass an address as a
    string, the service will geocode the string and convert it to a
    latitude/longitude coordinate to calculate directions.
:type destinations: a single location, or a list of locations, where a
    location is a string, dict, list, or tuple
:param mode: Specifies the mode of transport to use when calculating
    directions. Valid values are "driving", "walking", "transit" or
    "bicycling".
:type mode: string
:param language: The language in which to return results.
:type language: string
:param avoid: Indicates that the calculated route(s) should avoid the
    indicated features. Valid values are "tolls", "highways" or "ferries".
:type avoid: string
:param units: Specifies the unit system to use when displaying results.
    Valid values are "metric" or "imperial".
:type units: string
:param departure_time: Specifies the desired time of departure.
:type departure_time: int or datetime.datetime
:param arrival_time: Specifies the desired time of arrival for transit
    directions. Note: you can't specify both departure_time and
    arrival_time.
:type arrival_time: int or datetime.datetime
:param transit_mode: Specifies one or more preferred modes of transit.
    This parameter may only be specified for requests where the mode is
    transit. Valid values are "bus", "subway", "train", "tram", "rail".
    "rail" is equivalent to ["train", "tram", "subway"].
:type transit_mode: string or list of strings
:param transit_routing_preference: Specifies preferences for transit
    requests. Valid values are "less_walking" or "fewer_transfers".
:type transit_routing_preference: string
:param traffic_model: Specifies the predictive travel time model to use.
    Valid values are "best_guess" or "optimistic" or "pessimistic".
    The traffic_model parameter may only be specified for requests where
    the travel mode is driving, and where the request includes a
    departure_time.
:param region: Specifies the prefered region the geocoder should search
    first, but it will not restrict the results to only this region. Valid
    values are a ccTLD code.
:type region: string
:rtype: matrix of distances. Results are returned in rows, each row
    containing one origin paired with each destination.
"""

# Bronte Beach	Nature	Sydney	UTC	29	-33.90341	151.26839
# Chinese Garden of Friendship	Culture	Sydney	UTC	10	-33.876508	151.202797


geo_distance = gmaps.distance_matrix(origins = "-33.90341,151.26839", destinations="-33.876508,151.202797",
                                     mode="driving", language="en", departure_time=datetime.now())

print(geo_distance)