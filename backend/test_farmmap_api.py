#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from datetime import datetime
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# API 정보 - 환경변수에서 가져오기
service_key = os.getenv('FARMMAP_SERVICE_KEY')
encoded_key = os.getenv('FARMMAP_ENCODED_KEY')

# 기본 엔드포인트 (문서 기준)
base_url = "http://apis.data.go.kr/B552895/rest/farmmap/getFarmmapAgricultureWeatherService"

print("=" * 80)
print("팜맵(Farmmap) 기반 농업기상 조회 서비스 API 테스트")
print("=" * 80)
print("\n팜맵이란?")
print("- 항공/위성 영상과 현장 실사를 통해 제작된 농경지 전자지도")
print("- 논, 밭, 과수, 시설물 등 실제 경작 현황을 반영")
print("- 지적도와 달리 실제 이용 형태 기준으로 구획")
print("-" * 80)

# 테스트 1: 좌표기반 시간별 농업기상 조회
print("\n[테스트 1] 좌표기반 시간별 농업기상 상세조회")
print("-" * 40)

params_time = {
    'serviceKey': encoded_key,
    'numOfRows': '10',
    'pageNo': '1',
    'type': 'json',
    'positionX': '1121355.550488932',
    'positionY': '1976977.084509703',
    'date': '20240915',  # 시간별은 date 파라미터 사용
    'yearCount': '1'
}

try:
    print(f"요청 URL: {base_url}")
    print(f"요청 파라미터: {params_time}")
    
    response = requests.get(base_url, params=params_time, timeout=15)
    print(f"\n응답 상태: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"응답 형식: JSON")
            print(f"응답 데이터:\n{json.dumps(data, indent=2, ensure_ascii=False)[:2000]}")
        except:
            print(f"응답 형식: XML 또는 기타")
            print(f"응답 내용:\n{response.text[:2000]}")
    else:
        print(f"오류 응답:\n{response.text[:1000]}")
        
except Exception as e:
    print(f"요청 실패: {e}")

# 테스트 2: 좌표기반 일별 농업기상 조회
print("\n" + "=" * 80)
print("[테스트 2] 좌표기반 일별 농업기상 상세조회")
print("-" * 40)

params_day = {
    'serviceKey': encoded_key,
    'numOfRows': '10',
    'pageNo': '1',
    'type': 'json',
    'positionX': '1121355.550488932',
    'positionY': '1976977.084509703',
    'month': '202409',  # 일별은 month 파라미터 사용
    'yearCount': '1'
}

try:
    print(f"요청 URL: {base_url}")
    print(f"요청 파라미터: {params_day}")
    
    response = requests.get(base_url, params=params_day, timeout=15)
    print(f"\n응답 상태: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"응답 형식: JSON")
            print(f"응답 데이터:\n{json.dumps(data, indent=2, ensure_ascii=False)[:2000]}")
        except:
            print(f"응답 형식: XML 또는 기타")
            print(f"응답 내용:\n{response.text[:2000]}")
    else:
        print(f"오류 응답:\n{response.text[:1000]}")
        
except Exception as e:
    print(f"요청 실패: {e}")

# 테스트 3: XML 형식으로 요청
print("\n" + "=" * 80)
print("[테스트 3] XML 형식 응답 테스트")
print("-" * 40)

params_xml = {
    'serviceKey': encoded_key,
    'numOfRows': '5',
    'pageNo': '1',
    'type': 'xml',  # XML 형식 요청
    'positionX': '1121355.550488932',
    'positionY': '1976977.084509703',
    'date': '20240915',
    'yearCount': '1'
}

try:
    print(f"요청 URL: {base_url}")
    print(f"요청 파라미터: {params_xml}")
    
    response = requests.get(base_url, params=params_xml, timeout=15)
    print(f"\n응답 상태: {response.status_code}")
    
    if response.status_code == 200:
        print(f"응답 내용 (처음 2000자):\n{response.text[:2000]}")
        
        # XML 파싱 시도
        try:
            root = ET.fromstring(response.text)
            print("\nXML 구조 분석:")
            for child in root:
                print(f"  - {child.tag}: {child.text if child.text else '하위 요소 포함'}")
        except:
            print("XML 파싱 실패")
    else:
        print(f"오류 응답:\n{response.text[:1000]}")
        
except Exception as e:
    print(f"요청 실패: {e}")

print("\n" + "=" * 80)
print("API 테스트 완료")
print("=" * 80)