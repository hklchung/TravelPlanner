import json

print('Loading function')

def lambda_handler(event, context):
    #==================1. Parse out query string parameters=====================
    userID = event['queryStringParameters']['userID']
    user_profile = event['queryStringParameters']['profile']
    usr_lat = event['queryStringParameters']['start_latlong'][0]
    usr_long = event['queryStringParameters']['start_latlong'][1]
    trip_day = event['queryStringParameters']['trip_date']
    trip_start = event['queryStringParameters']['trip_hours'][0]
    trip_end = event['queryStringParameters']['trip_hours'][1]
    trv_dist = event['queryStringParameters']['trv_dist']
    
    print('userID= ' + userID)
    print('user_profile= ' + user_profile)
    print('userLocation= ' + usr_lat + ',' + usr_long)
    print('tripDate= ' + trip_day)
    print('tripHours= ' + trip_start + ':' + trip_end)
    print('tripDistance= ' + trv_dist)
    
    #=================2. Construct body of response object======================
    locationRecommendation = {}
    locationRecommendation['locationName'] = 'Blackwattle Bay Reserve'
    locationRecommendation['category'] = 'Nature'
    locationRecommendation['latitude'] = '-33.871'
    locationRecommendation['longtitude'] = '151.185'
    locationRecommendation['usr_trav_dist'] = '9.13275'
    locationRecommendation['usr_trav_time'] = '01:00:00'
    locationRecommendation['overlap_time'] = '8'
    
    #=================3. Construct http response object=========================
    responseObject = {}
    responseObject['statusCode'] = 200
    #responseObject['headers'] {}
    #responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(locationRecommendation)
    
    #=================4. Return the response object=============================
    return responseObject