import requests
import json
from datetime import datetime
import urllib3
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# SSL 경고 비활성화
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# API 정보 - 환경변수에서 가져오기
service_key = os.getenv('FARMMAP_SERVICE_KEY')
encoded_key = os.getenv('FARMMAP_ENCODED_KEY')

# 기본 엔드포인트들 시도
endpoints = [
    "https://apis.data.go.kr/B552895/rest/farmmap/getFarmmapAgricultureWeatherService",
    "https://apis.data.go.kr/B552895/rest/farmmap/positionTimeWeatherDetail",
    "https://apis.data.go.kr/B552895/rest/farmmap/positionDayWeatherDetail",
    "https://apis.data.go.kr/B552895/farmmap/getFarmmapAgricultureWeatherService"
]

# 파라미터 설정
params = {
    'serviceKey': encoded_key,
    'numOfRows': '10',
    'pageNo': '1',
    'type': 'json',
    'positionX': '1121355.550488932',
    'positionY': '1976977.084509703',
    'date': '20240915',
    'yearCount': '1'
}

print("농림수산식품교육문화정보원 팜맵기반 농업기상 조회 서비스 테스트")
print("=" * 60)

for endpoint in endpoints:
    print(f"\n엔드포인트 테스트: {endpoint}")
    print("-" * 40)
    
    try:
        response = requests.get(endpoint, params=params, timeout=10)
        print(f"상태 코드: {response.status_code}")
        print(f"응답 헤더: {dict(response.headers)}")
        
        # 응답 내용 출력
        if response.status_code == 200:
            # JSON 파싱 시도
            try:
                data = response.json()
                print(f"JSON 응답:\n{json.dumps(data, indent=2, ensure_ascii=False)[:1000]}")
            except:
                # XML이거나 다른 형식일 경우
                print(f"텍스트 응답:\n{response.text[:1000]}")
        else:
            print(f"오류 응답:\n{response.text[:500]}")
            
    except requests.exceptions.RequestException as e:
        print(f"요청 실패: {e}")

# XML 형식으로도 테스트
print("\n\nXML 형식 테스트")
print("=" * 60)
params['type'] = 'xml'

response = requests.get(endpoints[0], params=params, timeout=10)
print(f"상태 코드: {response.status_code}")
print(f"응답 내용:\n{response.text[:1000]}")