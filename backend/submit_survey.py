import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# 시니어 설문 데이터
senior_survey = {
    "basic_info": {
        "address": "경기도 이천시 대월면",
        "crop": "포도",
        "experience": 30
    },
    "successor_pref": {
        "retirement_timeline": "1-3년",
        "priority": "계승 및 안정성"
    },
    "conditions": {
        "preferred_goal": "B",
        "scenario_choice": "B",
        "post_relationship": "멘토십"
    },
    "vision": {
        "consultation_channel": "지역 농협",
        "income_type": "연금 형태"
    }
}

# 청년 설문 데이터  
youth_survey = {
    "basic_info": {
        "region": "경기도",
        "crop": "포도",
        "experience": 1,
        "capital": 50000000
    },
    "vision_info": {
        "values": "계승 및 안정성",
        "short_term_goal": "기존 방식 유지하며 안정적 운영"
    },
    "partnership": {
        "philosophy_attitude": "완전히 존중",
        "mentorship_level": "밀접한 지도"
    },
    "finance": {
        "info_channel": "지역 농협",
        "funding_preference": "정부 지원금"
    }
}

def submit_surveys():
    print("설문 제출을 통한 프로필 생성")
    print("=" * 50)
    
    # 1. 시니어 로그인 및 설문 제출
    print("\n[시니어 설문 제출]")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": "senior001", "password": "password123"}
    )
    
    if login_response.status_code == 200:
        cookies = login_response.cookies
        print(f"시니어 로그인 성공: {login_response.json()['name']}")
        
        # 설문 제출
        survey_response = requests.post(
            f"{BASE_URL}/surveys/senior",
            json=senior_survey,
            cookies=cookies
        )
        
        if survey_response.status_code == 200:
            result = survey_response.json()
            print(f"시니어 설문 제출 성공")
            print(f"  - 프로필 ID: {result.get('profile_id')}")
            print(f"  - 철학 점수: {result.get('philosophy_score')}")
        else:
            print(f"설문 제출 실패: {survey_response.text}")
    
    # 2. 청년 로그인 및 설문 제출  
    print("\n[청년 설문 제출]")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": "youth001", "password": "password123"}
    )
    
    if login_response.status_code == 200:
        cookies = login_response.cookies
        print(f"청년 로그인 성공: {login_response.json()['name']}")
        
        # 설문 제출
        survey_response = requests.post(
            f"{BASE_URL}/surveys/youth",
            json=youth_survey,
            cookies=cookies
        )
        
        if survey_response.status_code == 200:
            result = survey_response.json()
            print(f"청년 설문 제출 성공")
            print(f"  - 프로필 ID: {result.get('profile_id')}")
            print(f"  - 철학 점수: {result.get('philosophy_score')}")
        else:
            print(f"설문 제출 실패: {survey_response.text}")
    
    print("\n" + "=" * 50)
    print("완료")

if __name__ == "__main__":
    submit_surveys()