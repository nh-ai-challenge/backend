import requests
import json

# 서버 URL
BASE_URL = "http://localhost:8000/api/v1"

# 테스트용 계정 정보
senior_user = {
    "username": "senior_test",
    "password": "test1234",
    "name": "김시니어",
    "user_type": "senior"
}

youth_user = {
    "username": "youth_test",
    "password": "test1234",
    "name": "이청년",
    "user_type": "youth"
}

def test_profile_api():
    print("=" * 50)
    print("프로필 API 테스트")
    print("=" * 50)
    
    # 1. 시니어 로그인
    print("\n[1] 시니어 계정 로그인")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": "senior001", "password": "password123"}
    )
    
    if login_response.status_code != 200:
        print("❌ 로그인 실패. 테스트 계정을 먼저 생성하세요.")
        return
    
    cookies = login_response.cookies
    print(f"✅ 로그인 성공: {login_response.json()['name']}")
    
    # 2. 프로필 조회
    print("\n[2] 내 프로필 조회")
    profile_response = requests.get(
        f"{BASE_URL}/profiles/me",
        cookies=cookies
    )
    
    if profile_response.status_code == 200:
        profile = profile_response.json()
        print(f"✅ 프로필 조회 성공")
        print(f"  - ID: {profile.get('id')}")
        print(f"  - 프로필 텍스트: {profile.get('profile_text', '없음')}")
        print(f"  - 임베딩 업데이트: {profile.get('embedding_updated_at', '없음')}")
    else:
        print(f"❌ 프로필 조회 실패: {profile_response.text}")
    
    # 3. 프로필 텍스트 업데이트
    print("\n[3] 프로필 텍스트 업데이트")
    profile_text = """
    30년간 포도 농사를 지어온 베테랑 농부입니다.
    친환경 재배에 대한 철학을 가지고 있으며,
    와인용 포도 품종 개발에도 관심이 많습니다.
    제 경험과 지식을 젊은 세대에게 전수하고 싶습니다.
    """
    
    update_response = requests.put(
        f"{BASE_URL}/profiles/me/profile-text",
        json={"profile_text": profile_text},
        cookies=cookies
    )
    
    if update_response.status_code == 200:
        result = update_response.json()
        print(f"✅ 프로필 텍스트 업데이트 성공")
        print(f"  - 임베딩 생성: {result.get('has_embedding')}")
        print(f"  - 메시지: {result.get('message')}")
    else:
        print(f"❌ 업데이트 실패: {update_response.text}")
    
    # 4. AI 프로필 요약 조회
    print("\n[4] AI 프로필 요약 조회")
    summary_response = requests.get(
        f"{BASE_URL}/profiles/me/profile-summary",
        cookies=cookies
    )
    
    if summary_response.status_code == 200:
        summary = summary_response.json()
        print(f"✅ AI 요약 생성 성공")
        print(f"  - 원본 텍스트: {summary.get('profile_text')[:50]}...")
        print(f"  - AI 요약:")
        print(f"    {summary.get('ai_summary')}")
    elif summary_response.status_code == 503:
        print("⚠️  AI 서비스 일시 사용 불가")
    else:
        print(f"❌ 요약 조회 실패: {summary_response.text}")
    
    print("\n" + "=" * 50)
    print("테스트 완료")
    print("=" * 50)

if __name__ == "__main__":
    test_profile_api()