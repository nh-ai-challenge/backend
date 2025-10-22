from fastapi import APIRouter, HTTPException, Depends
from app.schemas.land_prediction import LandPredictionRequest, LandPredictionResponse
from app.services.land_prediction import LandPredictionService

router = APIRouter()

# 토지 가격 예측 API 엔드포인트
@router.post("/land_prediction", response_model=LandPredictionResponse)
def predict_land_price(request: LandPredictionRequest,
                       service: LandPredictionService = Depends()):
    try:
        # service 예측 함수 호출 
        predicted_price = service.land_price_prediction(request)

        # 예측 결과 반환
        LandPredictionResponse(success=True, predicted_price=predicted_price)
        return {"토지 가격 예측 성공": predicted_price}
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")
    except Exception as e:
        return LandPredictionResponse(success=False, message=str(e))