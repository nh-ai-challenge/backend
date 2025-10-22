import joblib
import numpy as np
from app.schemas.land_prediction import LandPredictionRequest
import pandas as pd

# 모델 로드
model_path = "NH 농협 AI 아이디어 챌린지"

try:
    model = joblib.load(model_path)
    print("모델 로드 성공")
except FileNotFoundError:
    print(f"모델 파일을 찾을 수 없습니다: {model_path}")
    model = None

# 예측 로직 함수
def predict_land_price(data: LandPredictionRequest) -> float:
    if model is None:
        raise FileNotFoundError("모델이 로드되지 않았습니다.")
    
    # 입력 데이터를 DataFrame으로 변환
    input_data = pd.DataFrame([data.dict()])
    
    # 예측 수행
    prediction = model.predict(input_data)

    return float(prediction[0])

