import requests
import pprint
import json
import os
from datetime import datetime, timedelta

# 환경 변수에서 API 키를 가져옵니다.
RIP_API_KEY = os.getenv('RIP_API_KEY')

# 현재 날짜를 'YYYYMMDD' 형식으로 가져옵니다.
current_date = datetime.now().strftime('%Y%m%d')
beach_code = 'HAE'
data_type = 'ripCurrent'

# API 호출 URL을 설정합니다.
url = f"http://www.khoa.go.kr/api/oceangrid/ripCurrent/search.do?ServiceKey={RIP_API_KEY}&BeachCode={beach_code}&Date={current_date}&ResultType=json"

response = requests.get(url)
contents = response.text

if response.status_code == 200:
    # JSON 데이터 파싱
    result = response.json()
    
    # data와 meta를 분리
    data = result['result']['data']
    meta = result['result']['meta']
    
    # 가장 최신 시간을 가진 데이터를 선택
    latest_data = max(data, key=lambda x: datetime.strptime(x['obs_time'], '%Y-%m-%d %H:%M'))
    
    # 결과 출력
    print("Latest Data:")
    print(latest_data['score_msg'])
    score_msg = latest_data['score_msg']
    
    print("\nMeta:")
    print(meta)
    
    lon =(meta['lon'])
    lat = (meta['lat'])
    

else:
    print(f"Failed to retrieve data: {response.status_code}")


def get_variable_score_msg():
    return score_msg


def get_variable_meta():
    return meta

def get_variable_lon():
    return lon

def get_variable_lat():
    return lat
