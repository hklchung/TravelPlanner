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
        "trip_hours": [datetime.time(9,0), datetime.time(18,0)],
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
# Check in itin exists, if not, create a new one===============================
new_request = 0
try:
    itin
except NameError:
    column_names = ["time", "location", "latlong"]
    itin = pd.DataFrame(columns = column_names)
    
    new_request = 1
    #itin.loc[len(itin)] = [9, "Travelling", (usr_lat, usr_long)]
else:
    itin = itin

# Check if this is a new itinerary request=====================================
if new_request == 0:
    usr_lat, usr_long = itin['latlong'].iloc[-1][0],itin['latlong'].iloc[-1][1]

# Create a new recommendation list=============================================
rcmd = db.copy()

# Calculate travel distance from current location==============================
rcmd['usr_trav_dist'] = np.nan
for i in range(0, len(rcmd.index)):
        rcmd.iat[i,rcmd.columns.get_loc("usr_trav_dist")] = geopy.distance.geodesic((usr_lat, usr_long), 
                                                                        (rcmd['latitude'][i], rcmd['longtitude'][i])).km

# Filter locations based on travel distance====================================
if new_request == 1:
    if trv_dist == '1':
        rcmd = rcmd[rcmd['usr_trav_dist'] <= 5]
    elif trv_dist == '2':
        rcmd = rcmd[rcmd['usr_trav_dist'] <= 10]
    else:
        rcmd = rcmd[rcmd['usr_trav_dist'] <= 30]
elif new_request == 0:
    rcmd = rcmd[rcmd['usr_trav_dist'] <= 5]

rcmd.reset_index(inplace = True, drop = True)

# Estimate travel time to each location========================================
rcmd['usr_trav_time'] = np.nan
for i in range(0, len(rcmd)):
    if rcmd['usr_trav_dist'][i] <= 5:
        rcmd['usr_trav_time'][i] = datetime.time(0, 30)
    elif rcmd['usr_trav_dist'][i] > 5 and rcmd['usr_trav_dist'][i] <= 10:
        rcmd['usr_trav_time'][i] = datetime.time(1, 0)
    elif rcmd['usr_trav_dist'][i] > 10 and rcmd['usr_trav_dist'][i] <= 30:
        rcmd['usr_trav_time'][i] = datetime.time(2, 0)

# Calclate max time can be spent at location===================================
rcmd['overlap_time'] = np.nan
for i in range(0, len(rcmd)):
    curr_time = trip_start.replace(hour = trip_start.hour + rcmd['usr_trav_time'][i].hour, 
                       minute = trip_start.minute + rcmd['usr_trav_time'][i].minute)
    rcmd['overlap_time'][i] = overlap_time(curr_time, trip_end, 
                                           rcmd[opening[int(trip_day)]][i], 
                                           rcmd[closing[int(trip_day)]][i])
    
# Filter out locations that are not available currently========================
rcmd = rcmd[rcmd[opening[int(trip_day)]] < curr_time]
rcmd.reset_index(inplace = True, drop = True)

# Sample 5 locations to present to user based on scores========================
rcmd['loc_score'] = np.nan
for i in range(0, len(rcmd)):
    rcmd['loc_score'][i] = random.uniform(max(float(scores[rcmd['category'][i]] - 0.2),0), 
                                          min(float(scores[rcmd['category'][i]] + 0.2),1))
rcmd["rank"] = rcmd["loc_score"].rank(ascending = False)
rcmd = rcmd[rcmd['rank'] <= 5]
rcmd.reset_index(inplace = True, drop = True)

# Present only the needed info to user=========================================
rcmd = rcmd[['name','category','latitude','longtitude','usr_trav_dist','usr_trav_time','overlap_time']]