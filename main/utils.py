import os
import requests
import json
from datetime import datetime

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

params = {
    'serviceKey': WEATHER_API_KEY,
    'pageNo': '1',
    'numOfRows': '1000',
    'dataType': 'JSON',
    'base_date': now.strftime('%Y%m%d'),  # 현재 날짜 설정
    'base_time': closest_base_time,
    'nx': '99',
    'ny': '75',
}
print(now.strftime('%Y%m%d'))
print(closest_base_time)

# API 요청 보내기
response = requests.get(api_url, params=params)

# 응답 상태 코드 확인
if response.status_code == 200:
    # 응답 JSON 데이터 파싱
    data = response.json()
    
    # 필요한 정보 추출 및 저장할 딕셔너리 초기화
    forecast_data = {}
    items = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
    
    if items:
        # 같은 base_date와 base_time에서 가장 가까운 Forecast Time 찾기
        base_date = now.strftime('%Y%m%d')
        forecast_times = sorted(set(item.get('fcstTime') for item in items if item.get('baseDate') == base_date and item.get('baseTime') == closest_base_time))
        closest_forecast_time = min(forecast_times, key=lambda ft: abs(int(ft) - int(current_time)))

        for item in items:
            if item.get('baseDate') == base_date and item.get('baseTime') == closest_base_time and item.get('fcstDate') == base_date and item.get('fcstTime') == closest_forecast_time:
                category = item.get('category')
                fcst_value = item.get('fcstValue')
                
                # 카테고리별로 값 저장
                forecast_data[category] = fcst_value

        # 저장된 데이터 출력
        for category, value in forecast_data.items():
            print(f"{category}: {value}")
    else:
        print("No forecast data available.")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

def get_weather_item():
    return forecast_data.items()




