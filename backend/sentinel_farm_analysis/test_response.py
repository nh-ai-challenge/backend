import json
from datetime import datetime, timedelta
from sentinelhub import SentinelHubRequest, DataCollection, MimeType, CRS, BBox, SHConfig
import numpy as np
import os
from dotenv import load_dotenv

# .env 파일 로드 (상위 디렉토리의 .env 파일)
load_dotenv(dotenv_path='../../.env')

# 인증 설정 - 환경변수에서 가져오기
config = SHConfig()
config.sh_client_id = os.getenv('SENTINEL_CLIENT_ID')
config.sh_client_secret = os.getenv('SENTINEL_CLIENT_SECRET')

def test_single_request():
    """단일 요청으로 응답 구조 확인"""
    
    # 경북 상주시 농지 좌표
    lat, lon = 36.4134, 128.1589
    bbox = BBox(bbox=[lon-0.005, lat-0.005, lon+0.005, lat+0.005], crs=CRS.WGS84)
    
    # 간단한 NDVI 계산 evalscript
    evalscript = """
    //VERSION=3
    function setup() {
        return {
            input: ["B04", "B08", "dataMask"],
            output: { bands: 1, sampleType: "FLOAT32" }
        };
    }
    
    function evaluatePixel(sample) {
        if (sample.dataMask == 0) return [0];
        
        let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
        return [ndvi];
    }
    """
    
    # 2024년 8월 데이터 요청
    request = SentinelHubRequest(
        evalscript=evalscript,
        input_data=[SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L2A,
            time_interval=('2024-08-01', '2024-08-31'),
            maxcc=0.1
        )],
        responses=[SentinelHubRequest.output_response('default', MimeType.TIFF)],
        bbox=bbox,
        size=[10, 10],  # 작은 사이즈로 테스트
        config=config
    )
    
    print("API 요청 중...")
    data = request.get_data()
    
    print(" 응답 구조 분석:")
    print(f"- 응답 타입: {type(data)}")
    print(f"- 배열 길이: {len(data)}")
    
    if len(data) > 0:
        ndvi_array = data[0]
        print(f"- 첫 번째 요소 타입: {type(ndvi_array)}")
        print(f"- 배열 형태: {ndvi_array.shape}")
        print(f"- 데이터 타입: {ndvi_array.dtype}")
        print(f"- 최솟값: {np.min(ndvi_array):.4f}")
        print(f"- 최댓값: {np.max(ndvi_array):.4f}")
        print(f"- 평균값: {np.mean(ndvi_array):.4f}")
        
        # 배열의 일부 값들 확인
        print(f"- 샘플 값들: {ndvi_array.flatten()[:5]}")
        
        return ndvi_array
    
    return None

def get_year_data():
    """2024년 12개월 데이터 수집"""
    
    lat, lon = 36.4134, 128.1589
    bbox = BBox(bbox=[lon-0.005, lat-0.005, lon+0.005, lat+0.005], crs=CRS.WGS84)
    
    evalscript = """
    //VERSION=3
    function setup() {
        return {
            input: ["B04", "B08", "dataMask"],
            output: { bands: 1, sampleType: "FLOAT32" }
        };
    }
    
    function evaluatePixel(sample) {
        if (sample.dataMask == 0) return [0];
        
        let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
        return [ndvi];
    }
    """
    
    monthly_data = []
    year = 2024
    
    for month in range(1, 13):
        try:
            # 각 월의 15일 기준 +-7일
            target_date = datetime(year, month, 15)
            start_date = (target_date - timedelta(days=7)).strftime('%Y-%m-%d')
            end_date = (target_date + timedelta(days=7)).strftime('%Y-%m-%d')
            
            request = SentinelHubRequest(
                evalscript=evalscript,
                input_data=[SentinelHubRequest.input_data(
                    data_collection=DataCollection.SENTINEL2_L2A,
                    time_interval=(start_date, end_date),
                    maxcc=0.1
                )],
                responses=[SentinelHubRequest.output_response('default', MimeType.TIFF)],
                bbox=bbox,
                size=[50, 50],
                config=config
            )
            
            ndvi_array = request.get_data()[0]
            valid_pixels = ndvi_array[ndvi_array > -1]  # 유효한 NDVI 값만
            
            if len(valid_pixels) > 0:
                result = {
                    "month": month,
                    "date_range": f"{start_date} to {end_date}",
                    "avg_ndvi": float(np.mean(valid_pixels)),
                    "min_ndvi": float(np.min(valid_pixels)),
                    "max_ndvi": float(np.max(valid_pixels)),
                    "std_ndvi": float(np.std(valid_pixels)),
                    "pixel_count": len(valid_pixels),
                    "array_shape": ndvi_array.shape,
                    "status": "success"
                }
                
                print(f" {month}월: NDVI = {result['avg_ndvi']:.4f}")
            else:
                result = {
                    "month": month,
                    "date_range": f"{start_date} to {end_date}",
                    "status": "no_valid_data"
                }
                print(f" {month}월: 유효 데이터 없음")
            
            monthly_data.append(result)
            
        except Exception as e:
            print(f" {month}월: 오류 - {str(e)}")
            monthly_data.append({
                "month": month,
                "status": "error",
                "error": str(e)
            })
    
    # JSON으로 저장
    with open('test_2024_data.json', 'w', encoding='utf-8') as f:
        json.dump(monthly_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 결과 저장: test_2024_data.json")
    return monthly_data

if __name__ == "__main__":
    print(" 단일 요청 테스트")
    print("=" * 30)
    test_single_request()
    
    print("\n\n 2024년 12개월 데이터 수집")
    print("=" * 30)
    get_year_data()