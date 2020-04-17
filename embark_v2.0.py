import pandas as pd
import numpy as np
import time as tm
from datetime import datetime
import geopy.distance
from trv_utils import *
pd.options.mode.chained_assignment = None 

'''
Step 1: Collect required data and initiates a request call
Each request call triggers the algorithm to recommend top 5 locations to user
based on (1) user profile information, (2) user session request information, 
and (3) status of current itinerary.

Below codes complete the following
i.   Get locations data
    - Current: get data from local .xlsx file
    - Future: create new func to get data from AWS database
ii.  Get user profile information
    - Current: user self-selected profile type + preset scores
    - Future: predictive models to personalise location recommendation
iii. Get user session request information
'''
# Get locations data
db = grab_local_files()

# Input from the web/app
user = {"profile": 'Nature Lover', 
        "start_latlong": list(test_latlong(False)),
        "trip_date": '16-04-2020',
        "trip_hours": [9, 18],
        "trv_dist": 2
        }

# Get user profile information
user_profile = user['profile']
scores = user_profile_scores(user_profile)

# Get user session request information
usr_lat = user['start_latlong'][0]
usr_long = user['start_latlong'][1]
trip_day = datetime.datetime.strptime(user['trip_date'], '%d-%m-%Y').weekday()
trip_start = user['trip_hours'][0]
trip_end = user['trip_hours'][1]
trv_dist = str(user['trv_dist'])

opening = ['', 'mon_o', 'tue_o', 'wed_o','thurs_o', 'fri_o', 'sat_o', 'sun_o']
closing = ['', 'mon_c', 'tue_c', 'wed_c','thurs_c', 'fri_c', 'sat_c', 'sun_c']

'''
Step 2: Initiate itinerary, top 5 locations and populate itinerary
In this step, we will first determine if an itinerary already exists and create
a new one if it does not already exist. Then we will make a request call to 
the algorithm to generate top 5 locations based on constraints defined in
step 1.
'''
# Check in itin exists, if not, create a new one
try:
    itin
except NameError:
    itin = pd.DataFrame()
else:
    itin = itin

