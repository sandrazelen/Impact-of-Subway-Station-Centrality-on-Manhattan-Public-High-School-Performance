import requests
import pandas as pd
import time

#Replace with API Key
API_key = "YOUR_API_KEY"

origins = [
    {'name': 'Van Cortlandt Park-242 St', 'lat': 40.889248, 'lng': -73.898583}, {'name': '238 St', 'lat': 40.884667, 'lng': -73.90087}, {'name': '231 St', 'lat': 40.878856, 'lng': -73.904834}, {'name': 'Marble Hill-225 St', 'lat': 40.874561, 'lng': -73.909831}, {'name': '215 St', 'lat': 40.869444, 'lng': -73.915279}, {'name': '207 St', 'lat': 40.864621, 'lng': -73.918822}, {'name': 'Dyckman St and Nagle Av', 'lat': 40.860531, 'lng': -73.925536}, {'name': '191 St', 'lat': 40.855225, 'lng': -73.929412}, {'name': '181 St and St Nicholas Av', 'lat': 40.849505, 'lng': -73.933596}, {'name': '168 St-Washington Hts', 'lat': 40.840556, 'lng': -73.940133}, {'name': '157 St', 'lat': 40.834041, 'lng': -73.94489}, {'name': '145 St and Broadway', 'lat': 40.826551, 'lng': -73.95036}, {'name': '137 St-City College', 'lat': 40.822008, 'lng': -73.953676}, {'name': '125 St and Broadway', 'lat': 40.815581, 'lng': -73.958372}, {'name': '116 St-Columbia University', 'lat': 40.807722, 'lng': -73.96411}, {'name': 'Cathedral Pkwy (110 St) and Broadway', 'lat': 40.803967, 'lng': -73.966847}, {'name': '103 St and Broadway', 'lat': 40.799446, 'lng': -73.968379}, {'name': '96 St and Broadway', 'lat': 40.793919, 'lng': -73.972323}, {'name': '86 St and Broadway', 'lat': 40.788644, 'lng': -73.976218}, {'name': '79 St and Broadway', 'lat': 40.783934, 'lng': -73.979917}, {'name': '72 St and Broadway', 'lat': 40.778453, 'lng': -73.98197}, {'name': '66 St-Lincoln Center', 'lat': 40.77344, 'lng': -73.982209}, {'name': '59 St-Columbus Circle', 'lat': 40.768272, 'lng': -73.981833}, {'name': '50 St and Broadway', 'lat': 40.761728, 'lng': -73.983849}, {'name': 'Times Sq-42 St', 'lat': 40.755356, 'lng': -73.987042}, {'name': '34 St-Penn Station', 'lat': 40.75133, 'lng': -73.992224}, {'name': '28 St and 7th Av', 'lat': 40.747215, 'lng': -73.993365}, {'name': '23 St and 7th Av', 'lat': 40.744081, 'lng': -73.995657}, {'name': '18 St', 'lat': 40.74104, 'lng': -73.997871}, {'name': '14 St and 6 Av', 'lat': 40.738027, 'lng': -73.998205}, {'name': 'Christopher St-Sheridan Sq', 'lat': 40.733422, 'lng': -74.002906}, {'name': 'Houston St', 'lat': 40.728251, 'lng': -74.005367}, {'name': 'Canal St and Varick St', 'lat': 40.722854, 'lng': -74.006277}, {'name': 'Franklin St', 'lat': 40.719318, 'lng': -74.006886}, {'name': 'Chambers St and West Broadway', 'lat': 40.715478, 'lng': -74.009266}, {'name': 'WTC Cortlandt', 'lat': 40.711835, 'lng': -74.012188}, {'name': 'Rector St', 'lat': 40.70722, 'lng': -74.013342}, {'name': 'South Ferry', 'lat': 40.702068, 'lng': -74.013664},
]

def create_batch(arr, batch_size):
    for i in range(0, len(arr), batch_size):
        yield arr[i:i + batch_size]
        
        
def get_distances(origins):
    
    for count, origin in enumerate(origins):
        if(count!=len(origins)-1):
            
            origin_str =f"{origin['lat']},{origin['lng']}"
            #print("origin: ", origin_str)
            
            
            dest = origins[count+1]
            #print("Destination: ", dest)
            destination_str = f"{dest['lat']},{dest['lng']}"
            #print("destination coord: ", destination_str)
        
            url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin_str}&destinations={destination_str}&mode=subway&key={API_key}"

            # Make the request
            response = requests.get(url)
            data = response.json()
            print(data,",")
            time.sleep(2)

get_distances(origins)
