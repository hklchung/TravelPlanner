import datetime

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