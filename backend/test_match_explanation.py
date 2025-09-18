import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_match_with_explanation():
    print("=" * 60)
    print("매칭 계산 및 AI 설명 테스트")
    print("=" * 60)
    
    # 시니어 로그인
    print("\n[1] 시니어 로그인")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": "senior001", "password": "password123"}
    )
    
    if login_response.status_code == 200:
        cookies = login_response.cookies
        user_info = login_response.json()
        print(f"✅ 로그인 성공: {user_info['name']}")
        
        # 매칭 계산 (시니어 -> 청년)
        print("\n[2] 매칭 점수 계산 및 AI 설명 생성")
        
        # 청년 ID 가져오기 (하드코딩 대신 실제로는 리스트에서 선택)
        youth_id = "ab0c42e7-f192-4e15-9bdc-f3ea3a9885d4"  # youth001의 ID
        senior_id = str(user_info['id'])
        
        calculate_response = requests.post(
            f"{BASE_URL}/matches/calculate",
            json={
                "senior_id": senior_id,
                "youth_id": youth_id
            },
            params={"generate_explanation": True},
            cookies=cookies
        )
        
        if calculate_response.status_code == 200:
            result = calculate_response.json()
            print(f"✅ 매칭 계산 완료")
            print(f"\n📊 SCI 점수: {result['sci_score']}점")
            print(f"\n📈 상세 궁합도:")
            comp = result['compatibility']
            print(f"  - 철학: {comp['philosophy']}점")
            print(f"  - 사업: {comp['business']}점")
            print(f"  - 멘토십: {comp['mentorship']}점")
            print(f"  - 재무: {comp['finance']}점")
            
            print(f"\n🤖 AI 설명:")
            if result.get('ai_explanation') and result['ai_explanation'] != "매칭 설명을 생성할 수 없습니다":
                explanation = result['ai_explanation']
                # 설명을 줄 단위로 나누어 출력
                lines = explanation.split('\n')
                for line in lines[:20]:  # 처음 20줄만 출력
                    print(f"  {line}")
                if len(lines) > 20:
                    print(f"  ... (총 {len(lines)}줄)")
            else:
                print(f"  {result.get('ai_explanation', '설명 없음')}")
            
            match_id = result['match_id']
            
            # 매칭 상세 조회
            print("\n" + "=" * 60)
            print("[3] 매칭 상세 조회 (AI 설명 포함)")
            print("=" * 60)
            
            detail_response = requests.get(
                f"{BASE_URL}/matches/{match_id}",
                params={"generate_explanation": True},
                cookies=cookies
            )
            
            if detail_response.status_code == 200:
                detail = detail_response.json()
                print(f"✅ 매칭 상세 조회 성공")
                print(f"\n파트너: {detail['partner_name']} ({detail['partner_type']})")
                print(f"매칭 상태: {detail['status']}")
                
                if detail.get('ai_explanation'):
                    print(f"\n🤖 AI 상세 설명 (재생성):")
                    lines = detail['ai_explanation'].split('\n')
                    for line in lines[:10]:
                        print(f"  {line}")
            else:
                print(f"❌ 상세 조회 실패: {detail_response.text}")
                
        else:
            print(f"❌ 매칭 계산 실패: {calculate_response.text}")
    
    print("\n" + "=" * 60)
    print("테스트 완료")
    print("=" * 60)

if __name__ == "__main__":
    test_match_with_explanation()