from pydantic import BaseModel
from typing import Optional

# api 요청에 필요한 데이터 모델 
# 사용자가 입력할 피쳐 
# 토지 가격 예측 요청에 사용될 스키마
class LandPredictionRequest(BaseModel):
    행정구역명: str
    면적: float
    운영경력: float
    주요작물: str

# api 응답에 필요한 데이터 모델
class LandPredictionResponse(BaseModel):
    success: bool
    predicted_price: float
    message: Optional[str] = "예측을 완료했습니다."