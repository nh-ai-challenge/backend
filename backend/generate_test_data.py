import requests
import random
import json
from faker import Faker

fake = Faker('ko_KR')
BASE_URL = "http://localhost:8000/api/v1"

# 테스트 데이터 설정
CROPS = ["포도", "딸기", "사과", "배", "복숭아", "토마토", "벼", "고추", "배추", "감자"]
REGIONS = ["경기도", "강원도", "충청북도", "충청남도", "전라북도", "전라남도", "경상북도", "경상남도", "제주도"]
VALUES = ["수익성 및 성장성", "계승 및 안정성", "사회적 가치", "신속한 전환"]
RETIREMENT = ["1년 내", "1-3년", "3-5년", "미정"]
SHORT_GOALS = ["규모 확대 및 현대화", "기존 방식 유지하며 안정적 운영", "친환경/유기농 전환", "새로운 작물/기술 도입"]

def generate_senior_data(num_seniors=10):
    seniors = []
    for i in range(num_seniors):
        username = f"senior_{i+100}"
        password = "test1234"
        name = fake.name()
        
        # 프로필 텍스트 생성
        experience_years = random.randint(15, 40)
        crop = random.choice(CROPS)
        profile_texts = [
            f"{experience_years}년간 {crop} 농사를 지어온 베테랑 농부입니다. 친환경 재배에 대한 철학을 가지고 있으며, 후계자에게 제 노하우를 전수하고 싶습니다.",
            f"농업을 천직으로 여기며 {experience_years}년간 {crop} 재배에 헌신했습니다. 전통적인 농법과 현대 기술의 조화를 추구하며, 젊은 세대와 함께 성장하고 싶습니다.",
            f"{crop} 재배 전문가로 {experience_years}년의 경험을 보유하고 있습니다. 품질 우선주의를 고수하며, 열정 있는 청년 농부를 찾고 있습니다.",
            f"대를 이어 {crop} 농사를 지어왔으며, 이제는 의욕 있는 젊은이에게 농장을 물려주고자 합니다. 안정적인 승계를 최우선으로 생각합니다.",
            f"{experience_years}년 동안 {crop} 농사로 안정적인 수익을 창출해왔습니다. 사업적 마인드를 갖춘 청년과 함께 농장을 더욱 발전시키고 싶습니다."
        ]
        
        senior = {
            "username": username,
            "password": password,
            "name": name,
            "profile_text": random.choice(profile_texts),
            "survey_data": {
                "basic_info": {
                    "address": f"{random.choice(REGIONS)} {fake.city()}",
                    "crop": crop,
                    "experience": experience_years
                },
                "successor_pref": {
                    "retirement_timeline": random.choice(RETIREMENT),
                    "priority": random.choice(VALUES)
                },
                "conditions": {
                    "preferred_goal": random.choice(["A", "B"]),
                    "scenario_choice": random.choice(["A", "B"]),
                    "post_relationship": random.choice(["완전 독립", "멘토십", "공동 운영"])
                },
                "vision": {
                    "consultation_channel": random.choice(["지역 농협", "농업기술센터", "온라인 커뮤니티"]),
                    "income_type": random.choice(["연금 형태", "일시금", "수익 분배"])
                }
            }
        }
        seniors.append(senior)
    
    return seniors

def generate_youth_data(num_youths=10):
    youths = []
    for i in range(num_youths):
        username = f"youth_{i+100}"
        password = "test1234"
        name = fake.name()
        
        # 프로필 텍스트 생성
        prev_job = random.choice(["IT 개발자", "회계사", "마케터", "교사", "공무원", "대학생", "자영업자"])
        crop = random.choice(CROPS)
        profile_texts = [
            f"도시에서 {prev_job}로 일했지만, 자연과 함께하는 삶을 꿈꾸며 귀농을 결심했습니다. {crop} 재배에 관심이 많고, 열심히 배우고 싶습니다.",
            f"{prev_job} 경험을 살려 농업에 새로운 가치를 더하고 싶습니다. 스마트팜 기술을 활용한 효율적인 농업을 추구합니다.",
            f"젊은 열정과 새로운 아이디어로 농업의 미래를 만들어가고 싶습니다. {crop} 재배를 통해 지속가능한 농업을 실현하겠습니다.",
            f"귀농을 통해 제2의 인생을 시작하려 합니다. 선배님의 노하우를 배우며 {crop} 전문가로 성장하고 싶습니다.",
            f"{prev_job}에서 쌓은 경험과 농업에 대한 열정으로 새로운 도전을 시작합니다. 전통과 혁신이 조화를 이루는 농업을 추구합니다."
        ]
        
        youth = {
            "username": username,
            "password": password,
            "name": name,
            "profile_text": random.choice(profile_texts),
            "survey_data": {
                "basic_info": {
                    "region": random.choice(REGIONS),
                    "crop": crop,
                    "experience": random.randint(0, 5),
                    "capital": random.randint(30000000, 100000000)
                },
                "vision_info": {
                    "values": random.choice(VALUES),
                    "short_term_goal": random.choice(SHORT_GOALS)
                },
                "partnership": {
                    "philosophy_attitude": random.choice(["완전히 존중", "부분적 수용", "독자적 운영"]),
                    "mentorship_level": random.choice(["밀접한 지도", "주기적 조언", "독립적 운영"])
                },
                "finance": {
                    "info_channel": random.choice(["지역 농협", "온라인", "정부 기관"]),
                    "funding_preference": random.choice(["정부 지원금", "은행 대출", "자기 자본"])
                }
            }
        }
        youths.append(youth)
    
    return youths

def create_users_and_profiles(users_data, user_type):
    created_users = []
    
    for user_data in users_data:
        # 1. 회원가입
        register_data = {
            "username": user_data["username"],
            "password": user_data["password"],
            "name": user_data["name"],
            "user_type": user_type
        }
        
        register_response = requests.post(
            f"{BASE_URL}/auth/register",
            json=register_data
        )
        
        if register_response.status_code == 200:
            print(f"✅ {user_data['username']} 생성 완료")
            
            # 2. 로그인
            login_response = requests.post(
                f"{BASE_URL}/auth/login",
                json={
                    "username": user_data["username"],
                    "password": user_data["password"]
                }
            )
            
            if login_response.status_code == 200:
                cookies = login_response.cookies
                user_info = login_response.json()
                
                # 3. 설문 제출
                endpoint = f"/surveys/{user_type}"
                survey_response = requests.post(
                    f"{BASE_URL}{endpoint}",
                    json=user_data["survey_data"],
                    cookies=cookies
                )
                
                if survey_response.status_code == 200:
                    print(f"  ✅ 설문 제출 완료")
                    
                    # 4. 프로필 텍스트 업데이트
                    profile_response = requests.put(
                        f"{BASE_URL}/profiles/me/profile-text",
                        json={"profile_text": user_data["profile_text"]},
                        cookies=cookies
                    )
                    
                    if profile_response.status_code == 200:
                        print(f"  ✅ 프로필 텍스트 및 임베딩 생성 완료")
                        created_users.append({
                            "id": user_info["id"],
                            "username": user_data["username"],
                            "name": user_data["name"]
                        })
                    else:
                        print(f"  ❌ 프로필 텍스트 업데이트 실패")
                else:
                    print(f"  ❌ 설문 제출 실패: {survey_response.text}")
        elif "already exists" in register_response.text:
            print(f"⚠️  {user_data['username']} 이미 존재")
        else:
            print(f"❌ {user_data['username']} 생성 실패")
    
    return created_users

def main():
    print("=" * 60)
    print("대량 테스트 데이터 생성")
    print("=" * 60)
    
    # 시니어 데이터 생성
    print("\n[1] 시니어 농부 생성")
    print("-" * 40)
    senior_data = generate_senior_data(5)  # 5명 생성
    created_seniors = create_users_and_profiles(senior_data, "senior")
    
    # 청년 데이터 생성
    print("\n[2] 청년 농부 생성")
    print("-" * 40)
    youth_data = generate_youth_data(5)  # 5명 생성
    created_youths = create_users_and_profiles(youth_data, "youth")
    
    print("\n" + "=" * 60)
    print("생성 완료 요약")
    print("=" * 60)
    print(f"✅ 시니어 농부: {len(created_seniors)}명")
    print(f"✅ 청년 농부: {len(created_youths)}명")
    print(f"✅ 총 {len(created_seniors) + len(created_youths)}명의 테스트 사용자 생성")
    
    # 생성된 사용자 목록 저장
    with open("test_users.json", "w", encoding="utf-8") as f:
        json.dump({
            "seniors": created_seniors,
            "youths": created_youths,
            "timestamp": str(fake.date_time())
        }, f, ensure_ascii=False, indent=2)
    
    print("\n✅ test_users.json 파일에 사용자 목록 저장 완료")

if __name__ == "__main__":
    main()