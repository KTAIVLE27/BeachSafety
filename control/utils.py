import requests
import os
from main.models import Beach

def fetch_rip_current_data():
    # 환경 변수에서 API 키를 가져옵니다.
    api_key = os.getenv('RIP_API_KEY')
    url = f'http://www.khoa.go.kr/api/oceangrid/ripCurrentRecent/search.do?ServiceKey={api_key}&ResultType=json'
    response = requests.get(url)
    
    if response.status_code == 200:
        # JSON 데이터 파싱
        data = response.json()
        
        # 결과 데이터를 저장할 사전
        beach_data_dict = {}
        
        for beach in data['result']['data']:
            beach_code = beach['beach_code']
            beach_data_dict[beach_code] = {
                #'beach_name': beach['beach_name'],
                'obs_time': beach['obs_time'],
                #'water_temp': beach['water_temp'],
                #'air_temp': beach['air_temp'],
                #'wind_speed': beach['wind_speed'],
                'lon': beach['lon'],
                'lat': beach['lat'],
                #'wind_direct': beach['wind_direct'],
                #'wave_height': beach['wave_height'],
                #'wave_period': beach['wave_period'],
                'score_msg': beach['score_msg'],
                #'score': beach['score'],
            }
        print(beach_data_dict['HAE'])
        return beach_data_dict
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None




#이안류 위험 지수
def get_beach_score_msg(beach_API_CODE):  
    try:
        print('get_beach_score_msg')
        beach_data_dict = fetch_rip_current_data()
        return beach_data_dict[beach_API_CODE]['score_msg']
    except KeyError:
        return "NaN"  # 값이 없을 때 반환할 기본 메시지
    
def get_beach_lon(beach_name):
    try:
        beach = Beach.objects.get(beach_name=beach_name)
        return beach.beach_lon
    except Beach.DoesNotExist:
        return 0  # 값이 없을 때 반환할 기본 메시지

def get_beach_lat(beach_name):
    try:
        beach = Beach.objects.get(beach_name=beach_name)
        return beach.beach_lat
    except Beach.DoesNotExist:
        return 0  # 값이 없을 때 반환할 기본 메시지
    
    
def get_beach_obs_time(beach_API_CODE):
    try:
        beach_data_dict = fetch_rip_current_data()
        return beach_data_dict[beach_API_CODE]['obs_time']
    except KeyError:
        return "NaN"  # 값이 없을 때 반환할 기본 메시지
    