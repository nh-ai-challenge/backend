import google.generativeai as genai
from typing import Optional, Dict, Any
from app.core.config import settings
import logging
import json

logger = logging.getLogger(__name__)


class GeminiService:
    _initialized = False
    _model = None
    
    @classmethod
    def initialize(cls):
        if not cls._initialized and settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            cls._model = genai.GenerativeModel('gemini-1.5-flash')
            cls._initialized = True
            logger.info("Gemini API initialized successfully")
    
    @classmethod
    def generate_match_explanation(
        cls,
        senior_profile: Dict[str, Any],
        youth_profile: Dict[str, Any],
        sci_score: float,
        compatibility_details: Dict[str, float]
    ) -> Optional[str]:
        
        cls.initialize()
        if not cls._model:
            logger.warning("Gemini API not initialized - API key not provided")
            return None
        
        prompt = f"""
        다음 시니어 농부와 청년 농부의 매칭 결과를 자연스러운 한국어로 설명해주세요.
        
        시니어 농부 프로필:
        - 기본 정보: {json.dumps(senior_profile.get('basic_info', {}), ensure_ascii=False)}
        - 승계자 선호도: {json.dumps(senior_profile.get('successor_pref', {}), ensure_ascii=False)}
        - 승계 조건: {json.dumps(senior_profile.get('conditions', {}), ensure_ascii=False)}
        - 비전: {json.dumps(senior_profile.get('vision', {}), ensure_ascii=False)}
        - 자기소개: {senior_profile.get('profile_text', '없음')}
        
        청년 농부 프로필:
        - 기본 정보: {json.dumps(youth_profile.get('basic_info', {}), ensure_ascii=False)}
        - 비전 정보: {json.dumps(youth_profile.get('vision_info', {}), ensure_ascii=False)}
        - 파트너십: {json.dumps(youth_profile.get('partnership', {}), ensure_ascii=False)}
        - 재정: {json.dumps(youth_profile.get('finance', {}), ensure_ascii=False)}
        - 자기소개: {youth_profile.get('profile_text', '없음')}
        
        매칭 점수:
        - 전체 SCI 점수: {sci_score:.1f}점
        - 철학 궁합도: {compatibility_details.get('philosophy', 0):.1f}점
        - 사업 궁합도: {compatibility_details.get('business', 0):.1f}점
        - 멘토십 궁합도: {compatibility_details.get('mentorship', 0):.1f}점
        - 재무 궁합도: {compatibility_details.get('finance', 0):.1f}점
        
        다음 형식으로 설명해주세요:
        1. 매칭 강점 (2-3가지)
        2. 주의사항 (1-2가지)
        3. 성공 가능성 평가
        
        간결하고 긍정적인 톤으로 작성하되, 현실적인 조언도 포함해주세요.
        """
        
        try:
            response = cls._model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Failed to generate match explanation: {e}")
            return None
    
    @classmethod
    def generate_profile_summary(cls, profile_text: str, user_type: str) -> Optional[str]:
        
        cls.initialize()
        if not cls._model:
            return None
        
        role = "시니어 농부" if user_type == "senior" else "청년 농부"
        
        prompt = f"""
        다음 {role}의 자기소개를 읽고, 핵심 특징을 3줄로 요약해주세요:
        
        {profile_text}
        
        요약 형식:
        - 농업 철학/가치관
        - 강점/경험
        - 희망사항/목표
        """
        
        try:
            response = cls._model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Failed to generate profile summary: {e}")
            return None
    
    @classmethod
    def analyze_compatibility_factors(
        cls,
        senior_text: str,
        youth_text: str
    ) -> Optional[Dict[str, Any]]:
        
        cls.initialize()
        if not cls._model:
            return None
        
        prompt = f"""
        다음 두 농부의 자기소개를 분석하여 승계 궁합을 평가해주세요.
        
        시니어 농부:
        {senior_text}
        
        청년 농부:
        {youth_text}
        
        다음 항목을 JSON 형식으로 평가해주세요 (각 항목 0-100점):
        {{
            "philosophy_match": 점수,
            "experience_match": 점수,
            "communication_match": 점수,
            "vision_alignment": 점수,
            "key_strengths": ["강점1", "강점2"],
            "potential_challenges": ["도전과제1", "도전과제2"]
        }}
        """
        
        try:
            response = cls._model.generate_content(prompt)
            text = response.text
            
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0]
            elif '```' in text:
                text = text.split('```')[1].split('```')[0]
            
            return json.loads(text.strip())
        except Exception as e:
            logger.error(f"Failed to analyze compatibility: {e}")
            return None