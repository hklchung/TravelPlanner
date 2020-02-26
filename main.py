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
import json
# import request
import string
import time as tm
import datetime
from data import data
import geopy.distance

test_long = 151.239536 
test_lat = -33.939442


class Embark:

    def __init__(self):

        # Usr Long Lat - to do: geolocation
        self.usr_long = test_long
        self.usr_lat = test_lat


        print("Hello, how should we call you?")
        self.name = raw_input()

        print("{}, thanks for using Embark! How old are you?".format(self.name))
        print("Which day are you planning for a trip?")
        self.day = raw_input()
        print("Your trip will start from (time):")
        self.begin_hr = raw_input()
        print("Your trip will end at (time) :")
        self.end_hr = raw_input()
        print("How many locations would you like to visit?")
        self.loc_count = raw_input()
        print("How much time would you allow for travelling in total (in hours)?")
        self.trv_time = raw_input()
        print("Your first stop preference (short= 1, medium = 1, long = 2)? ")
        self.trv_dist = raw_input()
        print("What kind of activities do you prefer? Culture, Nightlife, Shopping, Theme Park, Nature?")
        self.pref = raw_input()
        print("Thanks for the information! We will now crunch some numbers and find locations that best suit your requirements!")

        self.usr_choice = ""
        self.first_long = 0
        self.first_lat = 0
        self.opening = ['', 'mon_o', 'tue_o', 'wed_o','thurs_o', 'fri_o', 'sat_o', 'sun_o']
        self.closing = ['', 'mon_c', 'tue_c', 'wed_c','thurs_c', 'fri_c', 'sat_c', 'sun_c']


    def get_google_client(self):
        pass


    def first_loc_candidate(self):
        db_temp = data

        # initialize db_temp column travel distance
        db_temp['usr_trav_dist'] = np.nan
        
        for i in range(0, len(db_temp.index)):
            db_temp.iat[i,db_temp.columns.get_loc("usr_trav_dist")] = geopy.distance.geodesic((self.usr_lat, self.usr_long), 
                                                                            (db_temp['latitude'][i], db_temp['longtitude'][i])).km
        if self.trv_dist == 0:
            rcmd1 = db_temp[db_temp['usr_trav_dist'] <= 5]
        elif self.trv_dist  == 1:
            rcmd1 = db_temp[db_temp['usr_trav_dist'] <= 10]
        else:
            rcmd1 = db_temp[db_temp['usr_trav_dist'] <= 20]
        return rcmd1
    
    def select_first(self):    
        first_loc = self.first_loc_candidate()
        print("We suggest the following to be your your first stop, pick one out of five!")
        print(first_loc.head(5))

        print("Which one will be your first stop? (0-5)")
        temp = raw_input()
        self.usr_choice = int(temp) - 1
        first_choice = first_loc.iloc[self.usr_choice]
        first_choice = first_choice.to_frame().transpose()
        print(first_loc.head())
        return first_choice, first_loc

    def overlap_time(self, usr_t1, usr_t2, loc_t1, loc_t2):
        start = datetime.datetime.combine(datetime.date.today(),max(loc_t1, usr_t1))
        end = datetime.datetime.combine(datetime.date.today(),min(loc_t2, usr_t2))
        delta = (end - start).total_seconds()/3600
        return delta


    def plan_trip(self):
        first_choice, rcmd = self.select_first()
        print(first_choice.head())
        plan_lat = first_choice['latitude'].iloc[0]
        plan_long = first_choice['longtitude'].iloc[0]
        rcmd_fil = rcmd.copy(deep=True)
        rcmd_fil.loc['trav_dist'] = np.nan
        # for i in range(0, len(rcmd_fil.index)):
        #     rcmd_fil.iat[i,rcmd_fil.columns.get_loc("trav_dist")] = geopy.distance.geodesic((plan_lat, plan_long), 
        #                                                                     (rcmd_fil['latitude'][i], rcmd_fil['longtitude'][i])).km
        # remove location that does not fit into users' timeframe
        
        o_time = []
        for i in range(0, len(rcmd_fil)):
            new = self.overlap_time(datetime.time(int(self.begin_hr)), 
                        datetime.time(int(self.end_hr)), 
                        rcmd_fil.iloc[i][self.opening[int(self.day)]], 
                        rcmd_fil.iloc[i][self.closing[int(self.day)]])
            o_time.append(new)
        rcmd_fil['o_time'] = o_time
        rcmd_fil = rcmd.loc[rcmd['o_time'] > 1]
        rcmd_fil_time = rcmd_fil.copy(deep=True)
        rcmd_fil_time = rcmd_fil[rcmd_fil[self.closing[int(self.day)]].apply(lambda x: x.hour) - int(self.begin_hr) > 2]
        

        # sort by distance (and should have a function to calculate the next stop according to the second stop, and so on)
        rcmd_fil_time = rcmd_fil_time.sort_values('trav_dist')

        sec_loc_count = int(self.loc_count) - 1

        if sec_loc_count > 0:
            rcmd_final = rcmd_fil_time[:sec_loc_count]

        else:
            rcmd_final = rcmd_fil_time[:1]

        return rcmd_final

    def print_itinerary(self):
        trip = self.plan_trip()
        print("Here is your itinerary! Enjoy your trip:")
        print(type(trip))

        # Call Google Map API to calculate actual travel time for each hotspot

def main():
    embark = Embark()
    embark.print_itinerary()



main()

    

