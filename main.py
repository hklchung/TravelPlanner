# step 1: get user info and preference (name, age, family, geolocation, number of free hour(s), start_time, end_time, travel_time)
# step 1.5: get user Google map client
# step 2: select the top 5 hotspot the user prefer, exclude the 4 other hotspots
# step 3: user select the first location
# step 4: use 1st hotspot location to determine the trip
# step 5: print the itinerary to user
# Optional: 
# step 6: allow the user to adjust the itinerary

import pandas as pd
import numpy as np
import time as tm
import datetime
import geopy.distance
from trv_utils import overlap_time
from trv_utils import update_itin
pd.options.mode.chained_assignment = None 

test_long = 151.239536 
test_lat = -33.939442

data_pwd = "../../Data/Sydney.xlsx"
db = pd.read_excel(data_pwd, sheet_name = 0, header = 0)
db = db[db['ready_f'] == 1]
db[['name', 'category', 'location','timezone_type']] = db[['name', 'category', 'location','timezone_type']].astype(str)
db[['timezone', 'postcode']] = db[['timezone', 'postcode']].astype(int)
db[['latitude', 'longtitude', 'cost_min', 'cost_max']] = db[['latitude', 'longtitude', 'cost_min', 'cost_max']].astype(float)
db[['free_f', 'indoor_f', 'outdoor_f', 'family_f']] = db[['free_f', 'indoor_f', 'outdoor_f', 'family_f']].astype(bool)
db = db.reset_index(drop=True)

class Embark:

    def __init__(self):

        # Need to use Google or something to find user real time location
        self.usr_long = test_long
        self.usr_lat = test_lat

        print("Hello, how should we call you?")
        self.name = input()

        print("{}, which day are you planning for a trip?".format(self.name))
        self.day = input()
        print("Your trip will start from (time):")
        self.begin_hr = input()
        print("Your trip will end at (time) :")
        self.end_hr = input()
        print("How many locations would you like to visit?")
        self.loc_count = input()
        print("How much time would you allow for travelling in total (in hours)?")
        self.trv_time = input()
        print("How far would you travel for your first stop (short= 1, medium = 2, long = 3)?")
        self.trv_dist = input()
        print("Thanks for the information! We will now crunch some numbers and find locations that best suit your requirements!")

        self.opening = ['', 'mon_o', 'tue_o', 'wed_o','thurs_o', 'fri_o', 'sat_o', 'sun_o']
        self.closing = ['', 'mon_c', 'tue_c', 'wed_c','thurs_c', 'fri_c', 'sat_c', 'sun_c']
        
        self.itin = pd.DataFrame()

    def get_google_client(self):
        pass

    def first_loc_candidate(self):
        db_temp = db.copy()

        # initialize db_temp column travel distance
        db_temp['usr_trav_dist'] = np.nan
        
        for i in range(0, len(db_temp.index)):
            db_temp.iat[i,db_temp.columns.get_loc("usr_trav_dist")] = geopy.distance.geodesic((self.usr_lat, self.usr_long), 
                                                                            (db_temp['latitude'][i], db_temp['longtitude'][i])).km
        if self.trv_dist == '1':
            rcmd1 = db_temp[db_temp['usr_trav_dist'] <= 5]
        elif self.trv_dist == '2':
            rcmd1 = db_temp[db_temp['usr_trav_dist'] <= 10]
        else:
            rcmd1 = db_temp[db_temp['usr_trav_dist'] <= 30]
        
        rcmd1['overlap'] = np.nan
        #error 
        rcmd1['overlap'] = rcmd1.apply(lambda x: overlap_time(int(self.begin_hr), 
             int(self.begin_hr) + 2, 
             x[self.opening[int(self.day)]], 
             x[self.closing[int(self.day)]]), axis=1)
        rcmd1 = rcmd1[rcmd1['overlap'] >= 2].sample(n = 5)
        rcmd1.reset_index(inplace = True, drop = True)
        return rcmd1
    
    def select_first(self):    
        first_loc = self.first_loc_candidate()
        print("These look like good spots to start your trip, pick one on the list!")
        print(first_loc['name'])
        print("Which one will be your first stop? (Pick from 0-4)")
        self.usr_choice = input()
        first_choice = pd.DataFrame(first_loc.iloc[int(self.usr_choice), :]).transpose()
        self.itin = update_itin(self.itin, first_choice)
        self.begin_hr = int(self.begin_hr) + 3 # ERROR: need to upate this to Google API, atm assumes spending 2 hours at loc and 1 hour travel
        self.trv_time = int(self.trv_time) - 1 # Error: assumes 1 hour travel time between every location
        return first_choice     

    def next_loc_candidate(self, n):
        self.itin.reset_index(inplace = True, drop = True)
        self.curr_lat = self.itin['latitude'][n]
        self.curr_long = self.itin['longtitude'][n]
        
        db_temp = db.copy()
        db_temp['usr_trav_dist'] = np.nan
        # Fina travel distance between current location and all other locations
        for i in range(0, len(db_temp.index)):
            db_temp.iat[i,db_temp.columns.get_loc("usr_trav_dist")] = geopy.distance.geodesic((self.curr_lat, self.curr_long), 
                                                                            (db_temp['latitude'][i], db_temp['longtitude'][i])).km
        
        rcmd2 = db_temp[db_temp['usr_trav_dist'] <= 10]
        # Final overlapping hours
        rcmd2['overlap'] = np.nan
        rcmd2['overlap'] = rcmd2.apply(lambda x: overlap_time(int(self.begin_hr), 
             int(self.begin_hr) + 2, 
             x[self.opening[int(self.day)]], 
             x[self.closing[int(self.day)]]), axis=1)
        rcmd2 = rcmd2[rcmd2['overlap'] >= 2].sample(n = 5)
        rcmd2.reset_index(inplace = True, drop = True)
        
        print("These look like good spots to go next, pick one on the list!")
        print(rcmd2['name'])
        print("Which one will be your first stop? (Pick from 0-4)")
        self.usr_choice = input()
        next_choice = pd.DataFrame(rcmd2.iloc[int(self.usr_choice), :]).transpose()
        
        self.itin = update_itin(self.itin, next_choice)
        self.begin_hr = int(self.begin_hr) + 3 # ERROR: need to upate this to Google API, atm assumes spending 2 hours at loc and 1 hour travel
        self.trv_time = int(self.trv_time) - 1 # Error: assumes 1 hour travel time between every location
        return next_choice
    
    def plan_trip(self):
        first = self.select_first()
        for i in range(0, int(self.loc_count)-1):
            next1 = self.next_loc_candidate(i)
        itin = self.itin
        return first, next1, itin

    def print_itinerary(self):
        _, _, trip = self.plan_trip()
        print("Here is your itinerary! Enjoy your trip:")
        print(trip.iloc[:, 0:2])

        # Call Google Map API to calculate actual travel time for each hotspot

def main():
    embark = Embark()
    embark.print_itinerary()



main()