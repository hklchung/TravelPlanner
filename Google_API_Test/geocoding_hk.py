import pandas as pd
import googlemaps


df_temp = pd.read_csv('geo_building_2.csv', encoding = 'utf-8')

gapi_key = 'API_KEY'
gmaps = googlemaps.Client(key=gapi_key)


loc_counter = 1
total = df_temp['location'].count()

i = 0

for location in df_temp['location']:
    address = location + ', Hong Kong'
    print('Processing {} / {} |'.format(loc_counter, total) + address)
    try:
        geocode_result = gmaps.geocode(address= location + 'Hong Kong')
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        print('lat: {} | lng: {} |'.format(lat, lng))
        df_temp.iat[i,df_temp.columns.get_loc("lat")] = lat
        df_temp.iat[i,df_temp.columns.get_loc("lng")] = lng
    except:
        i+=1
        continue
    
    i+=1
    loc_counter += 1


