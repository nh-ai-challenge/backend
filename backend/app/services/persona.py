from typing import Dict, List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.persona import Persona, PersonaType
from app.models.survey import Survey
from app.models.user import User
from app.data.questions import calculate_dimension_score


class PersonaService:
    
    @staticmethod
    def classify_persona(scores: Dict[str, float]) -> str:
        philosophy = scores.get('philosophy', 3)
        business = scores.get('business', 3)
        
        if philosophy <= 3 and business <= 3:
            return PersonaType.ARTISAN_SUCCESSOR
        elif philosophy <= 3 and business > 3:
            return PersonaType.EXPERIENCED_ENTREPRENEUR
        elif philosophy > 3 and business <= 3:
            return PersonaType.DATA_DRIVEN_ARTISAN
        else:
            return PersonaType.INNOVATIVE_MANAGER
    
    @staticmethod
    async def calculate_persona_from_surveys(
        db: AsyncSession, 
        user_id: UUID
    ) -> Optional[Persona]:
        query = select(Survey).where(Survey.user_id == user_id)
        result = await db.execute(query)
        surveys = result.scalars().all()
        
        if not surveys:
            return None
        
        dimensions = ['philosophy', 'business', 'mentorship', 'finance']
        scores = {}
        
        for dimension in dimensions:
            dim_surveys = [s for s in surveys if s.dimension == dimension]
            if dim_surveys:
                scores[dimension] = sum(s.score for s in dim_surveys) / len(dim_surveys)
            else:
                scores[dimension] = 3.0
        
        persona_type = PersonaService.classify_persona(scores)
        
        existing_persona = await db.execute(
            select(Persona).where(Persona.user_id == user_id)
        )
        persona = existing_persona.scalar_one_or_none()
        
        if persona:
            persona.persona_type = persona_type
            persona.philosophy_score = scores.get('philosophy', 3)
            persona.business_score = scores.get('business', 3)
            persona.mentorship_score = scores.get('mentorship', 3)
            persona.finance_score = scores.get('finance', 3)
        else:
            persona = Persona(
                user_id=user_id,
                persona_type=persona_type,
                philosophy_score=scores.get('philosophy', 3),
                business_score=scores.get('business', 3),
                mentorship_score=scores.get('mentorship', 3),
                finance_score=scores.get('finance', 3)
            )
            db.add(persona)
        
        await db.commit()
        await db.refresh(persona)
        return persona
    
    @staticmethod
    async def save_survey_answers(
        db: AsyncSession,
        user_id: UUID,
        answers: List[Dict]
    ) -> List[Survey]:
        saved_surveys = []
        
        for answer in answers:
            survey = Survey(
                user_id=user_id,
                question_id=answer['question_id'],
                question_text=answer.get('question_text', ''),
                answer=answer['answer'],
                score=answer.get('score'),
                dimension=answer.get('dimension')
            )
            db.add(survey)
            saved_surveys.append(survey)
        
        await db.commit()
        
        for survey in saved_surveys:
            await db.refresh(survey)
        
        return saved_surveys
    
    @staticmethod
    async def get_user_persona(
        db: AsyncSession,
        user_id: UUID
    ) -> Optional[Persona]:
        query = select(Persona).where(Persona.user_id == user_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @staticmethod
    def get_persona_description(persona_type: str) -> Dict[str, str]:
        descriptions = {
            PersonaType.ARTISAN_SUCCESSOR: {
                "name": "장인적 계승가",
                "core_values": "전통, 계승, 품질, 안정성",
                "description": "수십 년간 쌓아온 자신만의 노하우와 철학을 가장 중요하게 생각합니다. 농장은 돈벌이 수단 이전에 자부심이자 유산입니다."
            },
            PersonaType.EXPERIENCED_ENTREPRENEUR: {
                "name": "경험적 사업가",
                "core_values": "사업 수완, 확장, 경험, 수익",
                "description": "데이터나 신기술보다는 자신의 경험과 직관을 바탕으로 사업을 확장하고 수익을 내는 데 능숙합니다."
            },
            PersonaType.DATA_DRIVEN_ARTISAN: {
                "name": "데이터 기반 장인",
                "core_values": "정밀성, 데이터, 고품질, 효율화",
                "description": "최신 기술과 데이터를 활용하여 최고 품질의 농산물을 안정적으로 생산하는 것을 목표로 합니다."
            },
            PersonaType.INNOVATIVE_MANAGER: {
                "name": "혁신적 경영가",
                "core_values": "기술, 성장, 데이터, 수익 극대화",
                "description": "농업을 첨단 기술과 데이터로 무장한 '미래 산업'으로 봅니다. 스마트팜, AI, 빅데이터 등을 적극적으로 도입합니다."
            }
        }
        
        return descriptions.get(persona_type, {
            "name": "미분류",
            "core_values": "미정",
            "description": "아직 페르소나가 분류되지 않았습니다."
        })