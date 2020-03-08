import pandas as pd
import datetime
import random
import decimal

def overlap_time(usr_t1, usr_t2, loc_t1, loc_t2):
    usr_t1 = datetime.time(int(usr_t1))
    usr_t2 = datetime.time(int(usr_t2))
    start = datetime.datetime.combine(datetime.date.today(),max(loc_t1, usr_t1))
    end = datetime.datetime.combine(datetime.date.today(),min(loc_t2, usr_t2))
    delta = (end - start).total_seconds()/3600
    return delta

def update_itin(curr, new):
    updated = curr.append(new)
    return updated

def grab_local_files():
    data_pwd = "../../Data/Sydney.xlsx"
    db = pd.read_excel(data_pwd, sheet_name = 0, header = 0)
    db = db[db['ready_f'] == 1]
    db[['name', 'category', 'location','timezone_type']] = db[['name', 'category', 'location','timezone_type']].astype(str)
    db[['timezone', 'postcode']] = db[['timezone', 'postcode']].astype(int)
    db[['latitude', 'longtitude', 'cost_min', 'cost_max']] = db[['latitude', 'longtitude', 'cost_min', 'cost_max']].astype(float)
    db[['free_f', 'indoor_f', 'outdoor_f', 'family_f']] = db[['free_f', 'indoor_f', 'outdoor_f', 'family_f']].astype(bool)
    db = db.reset_index(drop=True)
    return(db)
    
def test_latlong(randomiser = True):
    if randomiser == True:
        test_lat = float(decimal.Decimal(random.randrange(-342264997, -334475017))/10000000)
        test_long = float(decimal.Decimal(random.randrange(1505255854, 1513464694))/10000000)
    else:
        test_long = float(151.239536)
        test_lat = float(-33.939442)
    return(test_lat, test_long)