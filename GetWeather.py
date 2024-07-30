import json
from datetime import datetime, timedelta
import requests  
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("weather")

def get_weather_data(city):  
    api_url = "http://api.weatherapi.com/v1/current.json"
    params = {  
        "q": city,    
        "key": "input_api_key_here"
    }  
    response = requests.get(api_url, params=params)  
    data = response.json()  
    return data  
    
def lambda_handler(event, context):

    cities = ["Kuala Lumpur", "George Town", "Johor Bahru", "Kuching"]
    for city in cities:
        data = get_weather_data(city)  
    
        temp = data['current']['temp_c']
        wind_speed = data['current']['wind_mph']
        wind_dir = data['current']['wind_dir']
        pressure_mb = data['current']['pressure_mb']
        humidity = data['current']['humidity']
    
        print(city, temp, wind_speed, wind_dir, pressure_mb, humidity)
        
        # Get the current UTC time and add 8 hours to convert to Malaysia time
        current_timestamp = datetime.utcnow() + timedelta(hours=8)
        
        date = current_timestamp.date().isoformat()
        hour = current_timestamp.hour
        minute = current_timestamp.minute
        time = current_timestamp.isoformat()  # Ensure the 'time' attribute is included
        
        item = {
                'city': city,
                'date': date,
                'hour': hour,
                'minute': minute,
                'time': time,  # Add the 'time' attribute
                'temp': temp,
                'wind_speed': wind_speed,
                'wind_dir': wind_dir,
                'pressure_mb': pressure_mb,
                'humidity': humidity
            }
        item = json.loads(json.dumps(item), parse_float=Decimal)
        # Insert data into DynamoDB
        table.put_item(
            Item=item
        )