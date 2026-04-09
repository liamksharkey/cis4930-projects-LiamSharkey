import csv
import json
import os
import numpy as np
import pandas as pd
import requests

out_path = 'data/processed/output.csv'

def main() :
    url_params = {'latitude': 41, 'longitude': -74,"daily": 
        ["temperature_2m_max", "temperature_2m_min", "sunrise", "sunset",
        "uv_index_max", "precipitation_sum", "wind_speed_10m_max",
        "wind_direction_10m_dominant", "precipitation_probability_max"]}
    
    base_url = 'https://api.open-meteo.com/v1/forecast'

    unwanted_data = ['generationtime_ms', 'utc_offset_seconds',
        'timezone_abbreviation', 'daily.time']
    
    #gets weather from new york down to columbia, not realistically
    #helpful
    while url_params["latitude"] > 0:
        try:
            r = requests.get(base_url, params = url_params)
            if r.status_code >= 400 and r.status_code < 500 :
                print("Client Error")
            elif r.status_code >= 500:
                print("Server Error")
            r.raise_for_status()
        except requests.exceptions.Timeout:
            print("Request timed out")
            return
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return
        
        print("Request Successful")
        
        #flatten out json so ever entry is a row
        df = pd.json_normalize(r.json())
        df.drop(columns=unwanted_data, inplace=True)
        df.fillna(np.nan, inplace=True)
        #temporary dataframe so we can take average

        #create header if the file doesn't exist yet
        if not(os.path.exists(out_path)):
            df.to_csv(out_path, index=False)
        else:
            df.to_csv(out_path, mode='a', header=False, index=False)

        url_params['latitude'] -= 20
    
if __name__ == '__main__':
    main()