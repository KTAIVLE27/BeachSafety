import requests
import os

# 환경 변수에서 API 키를 가져옵니다.
RIP_API_KEY = os.getenv('RIP_API_KEY')
url = f'http://www.khoa.go.kr/api/oceangrid/ripCurrentRecent/search.do?ServiceKey={RIP_API_KEY}&ResultType=json'

response = requests.get(url)
contents = response.text

if response.status_code == 200:
    # JSON 데이터 파싱
    data = response.json()
    
    # 결과 데이터를 저장할 사전
    beach_data_dict = {}
    
    for beach in data['result']['data']:
        beach_code = beach['beach_code']
        beach_data_dict[beach_code] = {
            'beach_name': beach['beach_name'],
            'obs_time': beach['obs_time'],
            'water_temp': beach['water_temp'],
            'air_temp': beach['air_temp'],
            'wind_speed': beach['wind_speed'],
            'lon': beach['lon'],
            'lat': beach['lat'],
            'wind_direct': beach['wind_direct'],
            'wave_height': beach['wave_height'],
            'wave_period': beach['wave_period'],
            'score_msg': beach['score_msg'],
            # 'score': beach['score'],
        }
    
    # 결과 출력
    # for beach_code, details in beach_data_dict.items():
    #     print(f"Beach Code: {beach_code}")
    #     for key, value in details.items():
    #         print(f"{key}: {value}")
    #     print("\n")
else:
    print(f"Failed to retrieve data: {response.status_code}")
    
# ['GYEONGPO', 'GORAEBUL','NAKSAN','DAECHON','MANGSANG','SOKCHO','SONGJUNG','IMRANG','JUNGMUN','HAE']

#이안류 위험 지수
def get_GYEONGPO_score_msg():
    return beach_data_dict['GYEONGPO']['score_msg']
def get_GORAEBUL_score_msg():
    return beach_data_dict['GORAEBUL']['score_msg']
def get_NAKSAN_score_msg():
    return beach_data_dict['NAKSAN']['score_msg']
def get_DAECHON_score_msg():
    return beach_data_dict['DAECHON']['score_msg']
def get_MANGSANG_score_msg():
    return beach_data_dict['MANGSANG']['score_msg']
def get_SOKCHO_score_msg():
    return beach_data_dict['SOKCHO']['score_msg']
def get_SONGJUNG_score_msg():
    return beach_data_dict['SONGJUNG']['score_msg']
def get_IMRANG_score_msg():
    return beach_data_dict['IMRANG']['score_msg']
def get_JUNGMUN_score_msg():
    return beach_data_dict['JUNGMUN']['score_msg']
def get_HAE_score_msg():
    return beach_data_dict['HAE']['score_msg']

#경도
def get_GYEONGPO_lon():
    return beach_data_dict['GYEONGPO']['lon']
def get_GORAEBUL_lon():
    return beach_data_dict['GORAEBUL']['lon']
def get_NAKSAN_lon():
    return beach_data_dict['NAKSAN']['lon']
def get_DAECHON_lon():
    return beach_data_dict['DAECHON']['lon']
def get_MANGSANG_lon():
    return beach_data_dict['MANGSANG']['lon']
def get_SOKCHO_lon():
    return beach_data_dict['SOKCHO']['lon']
def get_SONGJUNG_lon():
    return beach_data_dict['SONGJUNG']['lon']
def get_IMRANG_lon():
    return beach_data_dict['IMRANG']['lon']
def get_JUNGMUN_lon():
    return beach_data_dict['JUNGMUN']['lon']
def get_HAE_lon():
    return beach_data_dict['HAE']['lon']

#위도
def get_GYEONGPO_lat():
    return beach_data_dict['GYEONGPO']['lat']
def get_GORAEBUL_lat():
    return beach_data_dict['GORAEBUL']['lat']
def get_NAKSAN_lat():
    return beach_data_dict['NAKSAN']['lat']
def get_DAECHON_lat():
    return beach_data_dict['DAECHON']['lat']
def get_MANGSANG_lat():
    return beach_data_dict['MANGSANG']['lat']
def get_SOKCHO_lat():
    return beach_data_dict['SOKCHO']['lat']
def get_SONGJUNG_lat():
    return beach_data_dict['SONGJUNG']['lat']
def get_IMRANG_lat():
    return beach_data_dict['IMRANG']['lat']
def get_JUNGMUN_lat():
    return beach_data_dict['JUNGMUN']['lat']
def get_HAE_lat():
    return beach_data_dict['HAE']['lat']