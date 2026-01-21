"""
Image Generation Endpoint
"""
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import json

router = APIRouter()


@router.post("")
async def generate_image(request: Request):
    """
    이미지 생성 엔드포인트 - Image Generator Agent 호출
    """
    try:
        from app.services.orchestrator.image_generator.agent import run_image_generator
        
        body = await request.json()
        
        print(f"[DEBUG] ========== Image Generation 시작 ==========")
        print(f"[DEBUG] Request body: {json.dumps(body, ensure_ascii=False)[:200]}...")
        
        action = body.get('action', 'generate')
        user_id = body.get('user_id')
        text = body.get('text')
        image_base64 = body.get('image_base64')
        record_date = body.get('record_date')
        
        # Agent에게 명확한 요청 전달
        if action == 'generate':
            request_text = f"일기 텍스트로 이미지를 생성해주세요."
        elif action == 'upload':
            request_text = f"이미지를 S3에 업로드해주세요."
        elif action == 'prompt':
            request_text = f"일기 텍스트를 이미지 프롬프트로 변환해주세요."
        else:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": f"알 수 없는 action: {action}"
                }
            )
        
        result = run_image_generator(
            request=request_text,
            user_id=user_id,
            text=text,
            image_base64=image_base64,
            record_date=record_date
        )
        
        print(f"[DEBUG] Agent result: {json.dumps(result, ensure_ascii=False)[:200]}...")
        print(f"[DEBUG] ========== Image Generation 완료 ==========")
        return JSONResponse(content=result)
        
    except Exception as e:
        print(f"[ERROR] Image generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"이미지 생성 중 오류가 발생했습니다: {str(e)}"
            }
        )
