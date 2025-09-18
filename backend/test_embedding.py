import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.embedding import EmbeddingService
from app.services.gemini import GeminiService
import json

def test_embedding_service():
    print("=" * 50)
    print("1. 임베딩 서비스 테스트")
    print("=" * 50)
    
    # 테스트 텍스트
    senior_text = """
    저는 30년간 유기농 딸기 농사를 지어온 농부입니다. 
    땅과 작물을 사랑하며, 전통적인 농법과 현대 기술을 조화롭게 사용하고 있습니다.
    제 농장을 이어받을 젊은 농부를 찾고 있으며, 단순히 돈이 아닌 
    농업에 대한 열정과 철학을 공유할 수 있는 사람을 원합니다.
    """
    
    youth_text = """
    농업에 큰 관심을 가진 청년입니다. 도시에서 IT 일을 했지만
    자연과 함께하는 삶을 꿈꾸며 귀농을 준비하고 있습니다.
    스마트팜 기술을 활용한 효율적인 농업과 전통 농법의 가치를 
    모두 존중하며, 지속가능한 농업을 실현하고 싶습니다.
    """
    
    # 1. 임베딩 생성 테스트
    print("\n[임베딩 생성 테스트]")
    senior_embedding = EmbeddingService.generate_embedding(senior_text)
    youth_embedding = EmbeddingService.generate_embedding(youth_text)
    
    print(f"시니어 임베딩 차원: {len(senior_embedding) if senior_embedding else 'None'}")
    print(f"청년 임베딩 차원: {len(youth_embedding) if youth_embedding else 'None'}")
    
    if senior_embedding and youth_embedding:
        print(f"첫 5개 값 (시니어): {senior_embedding[:5]}")
        print(f"첫 5개 값 (청년): {youth_embedding[:5]}")
    
    # 2. 유사도 계산 테스트
    print("\n[유사도 계산 테스트]")
    if senior_embedding and youth_embedding:
        similarity = EmbeddingService.calculate_similarity(senior_embedding, youth_embedding)
        print(f"두 프로필 간 유사도: {similarity:.4f}")
        
        # 자기 자신과의 유사도 (1.0에 가까워야 함)
        self_similarity = EmbeddingService.calculate_similarity(senior_embedding, senior_embedding)
        print(f"자기 자신과의 유사도: {self_similarity:.4f}")
    
    # 3. 빈 텍스트 처리 테스트
    print("\n[빈 텍스트 처리 테스트]")
    empty_embedding = EmbeddingService.generate_embedding("")
    print(f"빈 텍스트 임베딩: {empty_embedding}")
    
    print("\n✅ 임베딩 서비스 테스트 완료")
    return True

def test_gemini_service():
    print("\n" + "=" * 50)
    print("2. Gemini 서비스 테스트")
    print("=" * 50)
    
    # API 키 확인
    from app.core.config import settings
    if not settings.GEMINI_API_KEY:
        print("⚠️  GEMINI_API_KEY가 설정되지 않았습니다.")
        return False
    
    print(f"API 키 설정됨: {settings.GEMINI_API_KEY[:10]}...")
    
    # 서비스 초기화
    GeminiService.initialize()
    
    # 1. 프로필 요약 테스트
    print("\n[프로필 요약 생성 테스트]")
    profile_text = """
    20년 경력의 포도 농부입니다. 친환경 재배를 고집하며,
    와인용 포도 품종 개발에 관심이 많습니다. 
    젊은 시절부터 쌓아온 노하우를 전수하고 싶습니다.
    """
    
    try:
        summary = GeminiService.generate_profile_summary(profile_text, "senior")
        if summary:
            print("생성된 요약:")
            print(summary)
        else:
            print("⚠️  요약 생성 실패")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    
    # 2. 궁합 분석 테스트
    print("\n[궁합 분석 테스트]")
    senior_text = "30년 전통 농법 고수, 품질 중시"
    youth_text = "IT 기술 활용, 효율성 추구"
    
    try:
        analysis = GeminiService.analyze_compatibility_factors(senior_text, youth_text)
        if analysis:
            print("궁합 분석 결과:")
            print(json.dumps(analysis, indent=2, ensure_ascii=False))
        else:
            print("⚠️  궁합 분석 실패")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    
    print("\n✅ Gemini 서비스 테스트 완료")
    return True

if __name__ == "__main__":
    print("NH Agri-Continuum 임베딩/AI 서비스 검증")
    print("=" * 50)
    
    # 임베딩 서비스 테스트
    embedding_ok = test_embedding_service()
    
    # Gemini 서비스 테스트  
    gemini_ok = test_gemini_service()
    
    print("\n" + "=" * 50)
    print("최종 검증 결과")
    print("=" * 50)
    print(f"임베딩 서비스: {'✅ 정상' if embedding_ok else '❌ 실패'}")
    print(f"Gemini 서비스: {'✅ 정상' if gemini_ok else '❌ 실패'}")