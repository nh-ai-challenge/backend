import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# 테스트 계정들
test_users = [
    {
        "username": "senior001",
        "password": "password123",
        "name": "김영철",
        "user_type": "senior"
    },
    {
        "username": "youth001", 
        "password": "password123",
        "name": "이하나",
        "user_type": "youth"
    }
]

def create_test_users():
    print("테스트 계정 생성")
    print("=" * 50)
    
    for user in test_users:
        print(f"\n{user['name']} ({user['user_type']}) 계정 생성 중...")
        
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=user
        )
        
        if response.status_code == 200:
            print(f"✅ {user['username']} 생성 완료")
        elif "already exists" in response.text:
            print(f"⚠️  {user['username']} 이미 존재함")
        else:
            print(f"❌ 실패: {response.text}")
    
    print("\n" + "=" * 50)
    print("완료")

if __name__ == "__main__":
    create_test_users()