import pandas as pd
import numpy as np
import time as tm
import datetime
import geopy.distance
from trv_utils import *
pd.options.mode.chained_assignment = None 

test_lat, test_long = test_latlong(False)
db = grab_local_files()

user_profile = "Nature Lover"
scores = user_profile_scores(user_profile)