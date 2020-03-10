from gcp_pwd import *
import googlemaps
import pandas as pd
from datetime import datetime

gmaps = googlemaps.Client(key=api)


def geo_trv_time(origin, dest, mode, depart_time):
    trv_info = gmaps.distance_matrix(origins = origin, destinations = dest,
                                     mode = mode, language = "en", departure_time = depart_time)
    trv_time = trv_info.get('rows')[0].get('elements')[0].get('duration_in_traffic').get('value')
    return(trv_time)
    
def geo_get_id(location_name):
    location_id = gmaps.find_place("The Star Casino", "textquery").get('candidates')[0].get('place_id')
    return(location_id)
    
def geo_get_rating(location_name):
    rating = gmaps.place(geo_get_id(location_name)).get('result').get('rating')
    return(rating)
    
#geo_trv_time(str(curr_loc['latitude'])+','+str(curr_loc['longtitude']),
#             str(dest_loc['latitude'])+','+str(dest_loc['longtitude']),
#             "driving",
#             datetime.now())