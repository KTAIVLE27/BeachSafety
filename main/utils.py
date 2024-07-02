# myapp/utils.py
# import os
# import requests
# from dotenv import load_dotenv
# import arrow

# api_key = os.getenv('WEATHER_API_KEY')
# if api_key is None:
#     print("Environment variable 'WEATHER_API_KEY' is not set.")
# else:
#     print(f"{api_key}")

# load_dotenv()

# WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
# WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

# api_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"

# params = {
#     'serviceKey': WEATHER_API_KEY,
#     'numOfRows': '10',
#     'dataType': 'JSON',
#     'base_time': '1800',
#     'nx': '99',
#     'ny': '75',
# }

import os
import requests
import json
from datetime import datetime

# 환경 변수에서 API 키 가져오기
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

# API URL 및 요청 매개 변수 설정
api_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"

params = {
    'serviceKey': WEATHER_API_KEY,
    'pageNo': '1',
    'numOfRows': '1000',
    'dataType': 'JSON',
    # 'base_date': datetime.now().strftime('%Y%m%d'),  # 현재 날짜 설정
    'base_date': 20240701,
    'base_time': '2300',
    'nx': '99',
    'ny': '75',
}

# API 요청 보내기
response = requests.get(api_url, params=params)

# 응답 상태 코드 확인
if response.status_code == 200:
    # 응답 JSON 데이터 파싱
    data = response.json()
    
    # 필요한 정보 추출 및 출력
    items = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
    
    if items:
        for item in items:
            base_date = item.get('baseDate')
            base_time = item.get('baseTime')
            category = item.get('category')
            fcst_date = item.get('fcstDate')
            fcst_time = item.get('fcstTime')
            fcst_value = item.get('fcstValue')
            nx = item.get('nx')
            ny = item.get('ny')
            
            print(f"Base Date: {base_date}, Base Time: {base_time}, Category: {category}, "
                  f"Forecast Date: {fcst_date}, Forecast Time: {fcst_time}, Value: {fcst_value}, "
                  f"nx: {nx}, ny: {ny}")
    else:
        print("No forecast data available.")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")



# def fetch_data_from_kma(current_time_kst, page_no, category, fcst_time):
#     try:
#         date_format = "YYYYMMDD"
#         base_date = current_time_kst.format(date_format)
#         params['base_date'] = base_date
#         params['pageNo'] = page_no

#         response = requests.get(api_url, params=params)
#         response.raise_for_status()
#         data = response.json()

#         items = data['response']['body']['items']['item']
#         found = next(filter(lambda x: x['category'] == category and x['fcstTime'] == fcst_time, items), None)

#         if found:
#             return found['fcstValue']
#         else:
#             return None

#     except requests.exceptions.HTTPError as errh:
#         print(f"HTTP Error: {errh}")
#     except requests.exceptions.ConnectionError as errc:
#         print(f"Error Connecting: {errc}")
#     except requests.exceptions.Timeout as errt:
#         print(f"Timeout Error: {errt}")
#     except requests.exceptions.RequestException as err:
#         print(f"Something went wrong: {err}")

#     return None

# import os
# import requests
# from datetime import datetime

# # 환경 변수에서 API 키 가져오기
# WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

# # API URL 설정
# api_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"

# def fetch_data_from_kma(current_time_kst, page_no, category, fcst_time):
#     try:
#         # base_date 설정
#         date_format = "%Y%m%d"
#         base_date = current_time_kst.format(date_format)
        
#         # 요청 매개 변수 설정
#         params = {
#             'serviceKey': WEATHER_API_KEY,
#             'pageNo': page_no,
#             'numOfRows': '1000',
#             'dataType': 'JSON',
#             'base_date': base_date,
#             'base_time': '1700',
#             'nx': '99',
#             'ny': '75',
#         }

#         # API 요청 보내기
#         response = requests.get(api_url, params=params)
#         response.raise_for_status()  # HTTP 에러 발생 시 예외 처리

#         # 응답 JSON 데이터 파싱
#         data = response.json()

#         # 필요한 정보 추출
#         items = data['response']['body']['items']['item']
#         found = next((item for item in items if item['category'] == category and item['fcstTime'] == fcst_time), None)

#         if found:
#             return found['fcstValue']
#         else:
#             return None

#     except requests.exceptions.HTTPError as errh:
#         print(f"HTTP Error: {errh}")
#     except requests.exceptions.ConnectionError as errc:
#         print(f"Error Connecting: {errc}")
#     except requests.exceptions.Timeout as errt:
#         print(f"Timeout Error: {errt}")
#     except requests.exceptions.RequestException as err:
#         print(f"Something went wrong: {err}")

#     return None