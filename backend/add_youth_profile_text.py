import requests

BASE_URL = "http://localhost:8000/api/v1"

def add_youth_profile_text():
    print("청년 프로필 텍스트 추가")
    print("=" * 50)
    
    # 청년 로그인
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": "youth001", "password": "password123"}
    )
    
    if login_response.status_code == 200:
        cookies = login_response.cookies
        print(f"✅ 청년 로그인 성공")
        
        # 프로필 텍스트 업데이트
        profile_text = """
        도시에서 IT 개발자로 5년간 일했지만, 자연과 함께하는 삶을 꿈꾸며 
        귀농을 결심했습니다. 스마트팜 기술에 관심이 많고, 
        데이터 분석을 통한 효율적인 농업을 추구합니다.
        전통적인 농업의 가치도 존중하며, 경험 많은 선배님께 
        배우고 싶은 열정이 가득합니다.
        """
        
        update_response = requests.put(
            f"{BASE_URL}/profiles/me/profile-text",
            json={"profile_text": profile_text},
            cookies=cookies
        )
        
        if update_response.status_code == 200:
            result = update_response.json()
            print(f"✅ 청년 프로필 텍스트 업데이트 성공")
            print(f"  - 임베딩 생성: {result.get('has_embedding')}")
        else:
            print(f"❌ 업데이트 실패: {update_response.text}")
    
    print("\n" + "=" * 50)
    print("완료")

if __name__ == "__main__":
    add_youth_profile_text()