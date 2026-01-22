# Secrets Manager 설정 가이드

## 필수 설정 키

```json
{
  "BEDROCK_REGION": "ap-northeast-2",
  "KB_REGION": "ap-northeast-2",
  "BEDROCK_MODEL_ARN": "arn:aws:bedrock:ap-northeast-2:324547056370:inference-profile/global.anthropic.claude-sonnet-4-5-20250929-v1:0",
  "BEDROCK_NOVA_CANVAS_MODEL_ID": "amazon.nova-canvas-v1:0",
  "NOVA_CANVAS_REGION": "us-east-1",
  "KNOWLEDGE_BASE_ID": "LOCNRTBMNB",
  "KNOWLEDGE_BASE_BUCKET": "knowledge-base-test-6575574"
}
```

## 키 설명

### BEDROCK_MODEL_ARN (필수)
- 모든 Claude 호출에 사용하는 모델 ARN
- Global Inference Profile ARN 권장
- 예: `arn:aws:bedrock:ap-northeast-2:324547056370:inference-profile/global.anthropic.claude-sonnet-4-5-20250929-v1:0`

### BEDROCK_NOVA_CANVAS_MODEL_ID (필수)
- 이미지 생성용 Nova Canvas 모델 ID
- 예: `amazon.nova-canvas-v1:0`

### BEDROCK_REGION (기본: ap-northeast-2)
- Claude 모델 호출 시 사용하는 리전
- Global Inference Profile 사용 시 자동으로 최적 리전 선택

### NOVA_CANVAS_REGION (기본: us-east-1)
- Nova Canvas는 US 리전에서만 사용 가능

### KB_REGION (기본: ap-northeast-2)
- Knowledge Base와 S3가 위치한 리전

### KNOWLEDGE_BASE_ID (필수)
- Bedrock Knowledge Base ID

### KNOWLEDGE_BASE_BUCKET (필수)
- S3 버킷 이름

## Global Inference Profile ARN 사용 (권장)

```
arn:aws:bedrock:ap-northeast-2:324547056370:inference-profile/global.anthropic.claude-sonnet-4-5-20250929-v1:0
```

**장점:**
- 자동으로 최적 리전 선택
- 더 나은 가용성과 성능
- 리전 장애 시 자동 페일오버

## 설정 업데이트 방법

### AWS CLI
```bash
aws secretsmanager update-secret \
  --secret-id agent-secret \
  --secret-string file://secret.json \
  --region ap-northeast-2
```

### AWS Console
1. Secrets Manager 콘솔 접속
2. `agent-secret` 선택
3. "Retrieve secret value" → "Edit"
4. JSON 형식으로 수정
5. "Save" 클릭

## 주의사항

- `BEDROCK_MODEL_ARN` 하나로 모든 Claude 호출 통일
- Nova Canvas는 반드시 US 리전 필요
- Knowledge Base와 S3는 같은 리전에 있어야 함


