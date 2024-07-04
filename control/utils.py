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
            #'beach_name': beach['beach_name'],
            #'obs_time': beach['obs_time'],
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
    
    #결과 출력
    # for beach_code, details in beach_data_dict.items():
    #     print(f"Beach Code: {beach_code}")
    #     for key, value in details.items():
    #         print(f"{key}: {value}")
    #     print("\n")
    
    #print(beach_data_dict['HAE']['lon'])
else:
    print(f"Failed to retrieve data: {response.status_code}")
    
# ['GYEONGPO', 'GORAEBUL','NAKSAN','DAECHON','MANGSANG','SOKCHO','SONGJUNG','IMRANG','JUNGMUN','HAE']

#이안류 위험 지수
def get_GYEONGPO_score_msg():
    try:
        return beach_data_dict['GYEONGPO']['score_msg']
    except KeyError:
        return "NaN"  # 값이 없을 때 반환할 기본 메시지
    
def get_GORAEBUL_score_msg():
    try:
        return beach_data_dict['GORAEBUL']['score_msg']
    except KeyError:
        return "NaN"  # 값이 없을 때 반환할 기본 메시지
def get_NAKSAN_score_msg():
    try:
        return beach_data_dict['NAKSAN']['score_msg']
    except KeyError:
        return "NaN"  # 값이 없을 때 반환할 기본 메시지

def get_DAECHON_score_msg():
    try:
        return beach_data_dict['DAECHON']['score_msg']
    except KeyError:
        return "NaN"  # 값이 없을 때 반환할 기본 메시지

def get_MANGSANG_score_msg():
    try:
        return beach_data_dict['MANGSANG']['score_msg']
    except KeyError:
        return "NaN"  # 값이 없을 때 반환할 기본 메시지
def get_SOKCHO_score_msg():
    try:
        return beach_data_dict['SOKCHO']['score_msg']
    except KeyError:
        return "NaN"  # 값이 없을 때 반환할 기본 메시지
def get_SONGJUNG_score_msg():
    try:
        return beach_data_dict['SONGJUNG']['score_msg']
    except KeyError:
        return "NaN"  # 값이 없을 때 반환할 기본 메시지
    
def get_IMRANG_score_msg():
    try:
        return beach_data_dict['IMRANG']['score_msg']
    except KeyError:
        return "NaN"  # 값이 없을 때 반환할 기본 메시지

def get_JUNGMUN_score_msg():
    try:
        return beach_data_dict['JUNGMUN']['score_msg']
    except KeyError:
        return "NaN"  # 값이 없을 때 반환할 기본 메시지
    
def get_HAE_score_msg():
    try:
        return beach_data_dict['HAE']['score_msg']
    except KeyError:
        return "NaN"  # 값이 없을 때 반환할 기본 메시지
   

#경도
def get_GYEONGPO_lon():
    try:
        return beach_data_dict['GYEONGPO']['lon']
    except KeyError:
        return 0  # 값이 없을 때 반환할 기본 메시지
def get_GORAEBUL_lon():
    try:
        return beach_data_dict['GORAEBUL']['lon']
    except KeyError:
        return 0  # 값이 없을 때 반환할 기본 메시지
def get_NAKSAN_lon():
    try:
        return beach_data_dict['NAKSAN']['lon']
    except KeyError:
        return 0  # 값이 없을 때 반환할 기본 메시지
def get_DAECHON_lon():
    try:
        return beach_data_dict['DAECHON']['lon']
    except KeyError:
        return 0  # 값이 없을 때 반환할 기본 메시지
def get_MANGSANG_lon():
    try:
        return beach_data_dict['MANGSANG']['lon']
    except KeyError:
        return 0  # 값이 없을 때 반환할 기본 메시지
def get_SOKCHO_lon():
    try:
        return beach_data_dict['SOKCHO']['lon']
    except KeyError:
        return 0  # 값이 없을 때 반환할 기본 메시지
def get_SONGJUNG_lon():
    try:
        return beach_data_dict['SONGJUNG']['lon']
    except KeyError:
        return 0  # 값이 없을 때 반환할 기본 메시지    
def get_IMRANG_lon():
    try:
        return beach_data_dict['IMRANG']['lon']
    except KeyError:
        return 0  # 값이 없을 때 반환할 기본 메시지    
def get_JUNGMUN_lon():
    try:
        return beach_data_dict['JUNGMUN']['lon']
    except KeyError:
        return 0  # 값이 없을 때 반환할 기본 메시지   

def get_HAE_lon():
    try:
        return beach_data_dict['HAE']['lon']
    except KeyError:
        return 0  # 값이 없을 때 반환할 기본 메시지   


#위도
def get_GYEONGPO_lat():
    try:
        return beach_data_dict['GYEONGPO']['lat']
    except KeyError:
        return 0  # 값이 없을 때 반환할 기본 메시지   
def get_GORAEBUL_lat():
    try:
        return beach_data_dict['GORAEBUL']['lat']
    except KeyError:
        return 0  # 값이 없을 때 반환할 기본 메시지   
def get_NAKSAN_lat():
    try:
        return beach_data_dict['NAKSAN']['lat']
    except KeyError:
        return 0  # 값이 없을 때 반환할 기본 메시지   
def get_DAECHON_lat():
    try:
        return beach_data_dict['DAECHON']['lat']
    except KeyError:
        return 0  # 값이 없을 때 반환할 기본 메시지   
def get_MANGSANG_lat():
    try:
        return beach_data_dict['MANGSANG']['lat']
    except KeyError:
        return 0  # 값이 없을 때 반환할 기본 메시지  
def get_SOKCHO_lat():
    try:
        return beach_data_dict['SOKCHO']['lat']
    except KeyError:
        return 0  # 값이 없을 때 반환할 기본 메시지
def get_SONGJUNG_lat():
    try:
        return beach_data_dict['SONGJUNG']['lat']
    except KeyError:
        return 0  # 값이 없을 때 반환할 기본 메시지

def get_IMRANG_lat():
    try:
        return beach_data_dict['IMRANG']['lat']
    except KeyError:
        return 0  # 값이 없을 때 반환할 기본 메시지
    
def get_JUNGMUN_lat():
    try:
        return beach_data_dict['JUNGMUN']['lat']
    except KeyError:
        return 0  # 값이 없을 때 반환할 기본 메시지
    
def get_HAE_lat():
    try:
        return beach_data_dict['HAE']['lat']
    except KeyError:
        return 0  # 값이 없을 때 반환할 기본 메시지
