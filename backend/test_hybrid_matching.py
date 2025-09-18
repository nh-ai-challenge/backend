import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_hybrid_matching():
    print("=" * 60)
    print("하이브리드 매칭 테스트 (임베딩 + SCI)")
    print("=" * 60)
    
    # 시니어 로그인
    print("\n[1] 시니어 로그인 및 하이브리드 매칭 조회")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": "senior001", "password": "password123"}
    )
    
    if login_response.status_code == 200:
        cookies = login_response.cookies
        user_info = login_response.json()
        print(f"✅ 로그인 성공: {user_info['name']} ({user_info['user_type']})")
        
        # 하이브리드 매칭 조회
        print("\n[2] 하이브리드 매칭 추천 조회")
        hybrid_response = requests.get(
            f"{BASE_URL}/matches/recommendations/hybrid",
            params={
                "limit": 5,
                "min_similarity": 0.5,
                "embedding_weight": 0.3
            },
            cookies=cookies
        )
        
        if hybrid_response.status_code == 200:
            recommendations = hybrid_response.json()
            
            if recommendations:
                print(f"✅ {len(recommendations)}개의 매칭 추천 발견\n")
                
                for i, rec in enumerate(recommendations, 1):
                    print(f"매칭 #{i}")
                    print(f"  후보 ID: {rec['candidate_id'][:8]}...")
                    print(f"  하이브리드 점수: {rec['hybrid_score']}점")
                    print(f"  - SCI 점수: {rec['sci_score']}점")
                    print(f"  - 텍스트 유사도: {rec['text_similarity']}%")
                    
                    comp = rec['compatibility']
                    print(f"  상세 궁합도:")
                    print(f"    - 철학: {comp['philosophy']}점")
                    print(f"    - 경험: {comp['experience']}점")
                    print(f"    - 재무: {comp['financial']}점")
                    print(f"    - 일정: {comp['timeline']}점")
                    print(f"    - 멘토십: {comp['mentorship']}점")
                    
                    if rec.get('ai_explanation') and rec['ai_explanation'] != "매칭 설명을 생성할 수 없습니다":
                        print(f"  AI 설명:")
                        explanation = rec['ai_explanation'][:200]
                        print(f"    {explanation}...")
                    print()
            else:
                print("⚠️  매칭 결과가 없습니다. 더 많은 프로필이 필요합니다.")
        else:
            error = hybrid_response.json()
            print(f"❌ 매칭 조회 실패: {error.get('detail', 'Unknown error')}")
    
    # 기존 SCI 매칭과 비교
    print("\n[3] 기존 SCI 매칭과 비교")
    if login_response.status_code == 200:
        sci_response = requests.get(
            f"{BASE_URL}/matches/recommendations",
            params={"limit": 5},
            cookies=cookies
        )
        
        if sci_response.status_code == 200:
            sci_matches = sci_response.json()
            if sci_matches:
                print(f"✅ 기존 SCI 매칭: {len(sci_matches)}개 발견")
                for match in sci_matches[:3]:
                    print(f"  - SCI 점수: {match.get('sci_score', 'N/A')}점")
            else:
                print("⚠️  기존 SCI 매칭 결과 없음")
    
    print("\n" + "=" * 60)
    print("테스트 완료")
    print("=" * 60)

if __name__ == "__main__":
    test_hybrid_matching()