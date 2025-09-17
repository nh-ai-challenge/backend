from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.survey import (
    SurveySubmit, 
    SurveyResponse, 
    PersonaResponse,
    QuestionResponse
)
from app.services.persona import PersonaService
from app.services.auth import AuthService
from app.data.questions import get_questions_by_user_type, SENIOR_QUESTIONS, YOUTH_QUESTIONS

router = APIRouter(prefix="/surveys", tags=["Surveys"])


async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    user = await AuthService.get_user_by_id(db, UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


@router.get("/questions", response_model=List[QuestionResponse])
async def get_survey_questions(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    user = await get_current_user(request, db)
    questions = get_questions_by_user_type(user.user_type)
    
    response = []
    for q in questions:
        response.append(QuestionResponse(
            id=q['id'],
            section=q['section'],
            text=q['text'],
            type=q['type'],
            options=q.get('options'),
            dimension=q.get('dimension'),
            order=q['order']
        ))
    
    return response


@router.post("/submit", response_model=List[SurveyResponse])
async def submit_survey(
    survey_data: SurveySubmit,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    user = await get_current_user(request, db)
    
    questions = get_questions_by_user_type(user.user_type)
    question_map = {q['id']: q for q in questions}
    
    processed_answers = []
    for answer in survey_data.answers:
        question = question_map.get(answer.question_id)
        if question:
            score = None
            if question.get('scoring') and answer.answer in question['scoring']:
                score = question['scoring'][answer.answer]
            
            processed_answers.append({
                'question_id': answer.question_id,
                'question_text': answer.question_text,
                'answer': answer.answer,
                'score': score,
                'dimension': question.get('dimension')
            })
    
    saved_surveys = await PersonaService.save_survey_answers(
        db, user.id, processed_answers
    )
    
    await PersonaService.calculate_persona_from_surveys(db, user.id)
    
    return saved_surveys


@router.get("/my-results", response_model=PersonaResponse)
async def get_my_survey_results(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    user = await get_current_user(request, db)
    
    persona = await PersonaService.get_user_persona(db, user.id)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Survey results not found. Please complete the survey first."
        )
    
    persona_info = PersonaService.get_persona_description(persona.persona_type)
    
    return PersonaResponse(
        id=persona.id,
        user_id=persona.user_id,
        persona_type=persona.persona_type,
        persona_name=persona_info['name'],
        persona_description=persona_info['description'],
        philosophy_score=persona.philosophy_score,
        business_score=persona.business_score,
        mentorship_score=persona.mentorship_score,
        finance_score=persona.finance_score,
        created_at=persona.created_at,
        updated_at=persona.updated_at
    )