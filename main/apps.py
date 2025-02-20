from django.apps import AppConfig
from django.db.utils import OperationalError
from django.apps import apps
from datetime import date

class mainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'main' 

    
    def ready(self):
        Beach = apps.get_model('main', 'Beach') 
        CCTV = apps.get_model('main', 'CCTV') 
        User = apps.get_model('main', 'User') 

        # 해수욕장 데이터
        try:
            if not Beach.objects.exists():
                beaches = [
                    {"beach_name": "경포 해수욕장", "beach_region": "강릉시", "beach_lat": 37.8, "beach_lon": 128.909, "nx": 92, "ny": 132, "beach_widget_id": "wl7437",  "mae":6.2, "mse":72.73, "r2score" : 0.89, "beach_api_code":"GYEONGPO"},
                    {"beach_name": "고래불 해수욕장", "beach_region": "영덕군", "beach_lat": 36.597, "beach_lon": 129.411, "nx": 103, "ny": 107, "beach_widget_id": "wl7463",  "mae":6.12, "mse":76.28, "r2score" : 0.95, "beach_api_code":"GORAEBUL"},
                    {"beach_name": "낙산 해수욕장", "beach_region": "양양시", "beach_lat": 38.118, "beach_lon": 128.631, "nx": 87, "ny": 140, "beach_widget_id": "wl7478", "mae":5.7, "mse":63.61, "r2score" : 0.92, "beach_api_code":"NAKSAN"},
                    {"beach_name": "대천 해수욕장", "beach_region": "보령시", "beach_lat": 36.305, "beach_lon": 126.507, "nx": 53, "ny": 100, "beach_widget_id": "wl7459", "mae":3.98, "mse":32.18, "r2score" : 0.91, "beach_api_code":"DAECHON"},
                    {"beach_name": "망상 해수욕장", "beach_region": "동해시", "beach_lat": 37.593, "beach_lon": 129.09, "nx": 96, "ny": 127, "beach_widget_id": "wl7462", "mae":6.17, "mse":80.02, "r2score" : 0.94, "beach_api_code":"MANGSANG"},
                    {"beach_name": "속초 해수욕장", "beach_region": "속초시", "beach_lat": 38.19, "beach_lon": 128.601, "nx": 87, "ny": 140, "beach_widget_id": "wl7463", "mae":5.08, "mse":53.32, "r2score" : 0.95, "beach_api_code":"SOKCHO"},
                    {"beach_name": "송정 해수욕장", "beach_region": "부산광역시", "beach_lat": 35.178, "beach_lon": 129.199, "nx": 61, "ny": 126, "beach_widget_id": "wl1419", "mae":8.5, "mse":151.13, "r2score" : 0.77, "beach_api_code":"SONGJUNG"},
                    {"beach_name": "임랑 해수욕장", "beach_region": "부산광역시", "beach_lat": 35.318, "beach_lon": 129.264, "nx": 101, "ny": 79, "beach_widget_id": "wl1419", "mae":5.77, "mse":77.83, "r2score" : 0.94, "beach_api_code":"IMRANG"},
                    {"beach_name": "중문 해수욕장", "beach_region": "제주도", "beach_lat": 33.245, "beach_lon": 126.409, "nx": 51, "ny": 32,  "beach_widget_id": "wl7440", "mae":4.93, "mse":52.32, "r2score" : 0.97, "beach_api_code":"JUNGMUN"},
                    {"beach_name": "해운대 해수욕장", "beach_region": "부산광역시", "beach_lat": 35.158, "beach_lon": 129.16, "nx": 99, "ny": 75, "beach_widget_id": "wl1419", "mae":6.96, "mse":86.67, "r2score" : 0.92, "beach_api_code":"HAE"},
                    {"beach_name": "함덕 해수욕장", "beach_region": "제주도", "beach_lat": 33.543, "beach_lon": 126.669},
                    
                ]
                for beach in beaches:
                    Beach.objects.create(**beach)
                    print(f"{beach['beach_name']}의 데이터가 생성되었습니다.")
        except OperationalError:
            pass
        
        
        
        # CCTV 데이터
        try:
            if not CCTV.objects.exists():
                cctves = [
                    {"cctv_location": "함덕해수욕장", "cctv_url": "http://www.trendworld.kr/cctv/hamdeok.php", "beach_no_id" : 11},
                    {"cctv_location": "중문해수욕장", "cctv_url": "http://www.trendworld.kr/cctv/jungmunhaesuyokjang.php", "beach_no_id" : 9},
                ]
                for cctv in cctves:
                    beach_instance = Beach.objects.get(pk=cctv['beach_no_id'])
                    CCTV.objects.create(
                        cctv_location=cctv['cctv_location'],
                        cctv_url=cctv['cctv_url'],
                        beach_no=beach_instance
                    )
                    print(f"{cctv['cctv_location']}의 CCTV 데이터가 생성되었습니다.")
        except OperationalError:
            pass
        
        
        # 회원 데이터
        try:
            if not User.objects.filter(user_id='admin').exists():
                if not User.objects.filter(user_email='admin@aivle.com').exists():
                    user = User.objects.create_user(
                        user_id='admin',
                        user_email='admin@aivle.com',
                        user_joinday = date(2024, 7, 9),
                        user_name='김관리',
                        user_phone='010-0000-0000',
                        user_birth=date(1990, 1, 1),
                        user_address='광주 광역시 북구',
                        user_detail_address='KT 신안 본사',
                        user_role='admin',
                    )
                    user.set_password("aivle202405!")
                    user.save()
                    print("Admin user 생성되었습니다.")
            if not User.objects.filter(user_id='supervisor').exists():
                if not User.objects.filter(user_email='supervisor@aivle.com').exists():
                    user = User.objects.create_user(
                        user_id='supervisor',
                        user_email='supervisor@aivle.com',
                        user_joinday = date(2024, 7, 9),
                        user_name='박관제',
                        user_phone='010-1111-0000',
                        user_birth=date(1998, 1, 1),
                        user_address='광주 광역시 북구',
                        user_detail_address='KT 신안 본사',
                        user_role='supervisor',
                    )
                    user.set_password("aivle202405!")
                    user.save()
                    print("supervisor user 생성되었습니다.")
            if not User.objects.filter(user_id='police').exists():
                if not User.objects.filter(user_email='police@aivle.com').exists():
                    user = User.objects.create_user(
                        user_id='police',
                        user_email='police@aivle.com',
                        user_joinday = date(2024, 7, 9),
                        user_name='고경찰',
                        user_phone='010-2222-0000',
                        user_birth=date(1999, 1, 1),
                        user_address='광주 광역시 북구',
                        user_detail_address='KT 신안 본사',
                        user_role='police',
                    )
                    user.set_password("aivle202405!")
                    user.save()
                    print("police user 생성되었습니다.")
        except OperationalError:
            pass
                 
                 
    
        
        

