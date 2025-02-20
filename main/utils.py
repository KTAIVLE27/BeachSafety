import os
import requests
import json
from datetime import datetime
from .models import Beach
# 환경 변수에서 API 키 가져오기
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

# Base times schedule (8 times a day)
base_times = ['0200', '0500', '0800', '1100', '1400', '1700', '2000', '2300']

# 현재 시간 가져오기
now = datetime.now()
current_time = now.strftime('%H%M')

# 현재 시간에서 가장 가까운 지나간 시간 찾기
closest_base_time = max([bt for bt in base_times if bt <= current_time], default=base_times[0])

# API URL 및 요청 매개 변수 설정
api_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"

beach_records = Beach.objects.exclude(beach_name="함덕해수욕장")
beaches = [
    {"name": beach.beach_name, "nx": beach.nx, "ny": beach.ny}
    for beach in beach_records
]

# 날씨 데이터 가져오는 함수
def fetch_weather_data(beach):
    params = {
        'serviceKey': WEATHER_API_KEY,
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': 'JSON',
        'base_date': now.strftime('%Y%m%d'),  # 현재 날짜 설정
        'base_time': closest_base_time,
        'nx': beach['nx'],
        'ny': beach['ny'],
    }
    
    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        forecast_data = {}
        items = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
        
        if items:
            base_date = now.strftime('%Y%m%d')
            forecast_times = sorted(set(item.get('fcstTime') for item in items if item.get('baseDate') == base_date and item.get('baseTime') == closest_base_time))
            closest_forecast_time = min(forecast_times, key=lambda ft: abs(int(ft) - int(current_time)))

            for item in items:
                if item.get('baseDate') == base_date and item.get('baseTime') == closest_base_time and item.get('fcstDate') == base_date and item.get('fcstTime') == closest_forecast_time:
                    category = item.get('category')
                    fcst_value = item.get('fcstValue')
                    forecast_data[category] = fcst_value
            
            return forecast_data
        else:
            print(f"No forecast data available for {beach['name']}.")
            return None
    else:
        print(f"Failed to retrieve data for {beach['name']}. Status code: {response.status_code}")
        return None

# 모든 해수욕장의 날씨 데이터를 가져오는 함수
def fetch_all_beaches_weather():
    all_forecasts = {}
    for beach in beaches:
        forecast_data = fetch_weather_data(beach)
        if forecast_data:
            all_forecasts[beach['name']] = forecast_data
    
    return all_forecasts

# 데이터 출력
if __name__ == "__main__":
    weather_data = fetch_all_beaches_weather()
    for beach_name, forecast in weather_data.items():
        print(f"\n{beach_name} 날씨 정보:")
        for category, value in forecast.items():
            print(f"{category}: {value}")

def get_weather_item(beach_name):
    return weather_data.get(beach_name, {}).items()
