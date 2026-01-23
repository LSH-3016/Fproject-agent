# Phoenix Monitoring Guide

Arize Phoenix를 활용한 멀티 에이전트 AI 시스템 모니터링 가이드입니다.

## 개요

Phoenix는 LLM 애플리케이션의 관측성(Observability)을 제공하는 오픈소스 플랫폼입니다.

**주요 기능:**
- LLM 호출별 latency, 토큰 사용량 추적
- Agent tool 호출 순서와 시간 시각화
- 에러/실패 케이스 추적
- 프롬프트 → LLM 응답 → tool 실행 전체 trace 확인
- 응답 품질 평가 (hallucination, relevance)

## 로컬 개발 환경

### 1. Phoenix 서버 실행

```bash
docker-compose -f docker-compose.phoenix.yaml up -d
```

Phoenix UI: http://localhost:6006

### 2. 환경변수 설정

```bash
export PHOENIX_ENDPOINT=http://localhost:6006
export PHOENIX_PROJECT_NAME=diary-agent
export TRACING_ENABLED=true
```

### 3. 애플리케이션 실행

```bash
python run.py
```

## EKS 배포

### 1. Phoenix 리소스 배포

```bash
kubectl apply -f k8s/phoenix-configmap.yaml
kubectl apply -f k8s/phoenix-deployment.yaml
kubectl apply -f k8s/phoenix-service.yaml
```

### 2. Agent 배포 (트레이싱 환경변수 포함)

```bash
kubectl apply -f k8s/deployment.yaml
```

### 3. Phoenix UI 접근

```bash
kubectl port-forward svc/phoenix-service 6006:6006
```

브라우저에서 http://localhost:6006 접속

## 트레이스 조회

### Phoenix UI에서 확인 가능한 정보

1. **Traces 탭**: 전체 요청 흐름
   - Orchestrator → Sub-Agent → Tool 호출 순서
   - 각 단계별 소요 시간

2. **Spans 탭**: 개별 작업 상세
   - LLM 호출: 모델명, 토큰 수, latency
   - Tool 실행: 입력 파라미터, 실행 시간

3. **Evaluations 탭**: 응답 품질 평가
   - Hallucination 점수
   - Relevance 점수

## 환경변수 설정

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `PHOENIX_ENDPOINT` | Phoenix 서버 URL | `http://localhost:6006` |
| `PHOENIX_PROJECT_NAME` | 프로젝트 이름 | `diary-agent` |
| `TRACING_ENABLED` | 트레이싱 활성화 | `true` |
| `TRACE_SAMPLE_RATE` | 샘플링 비율 (0.0~1.0) | `1.0` |
| `DEBUG` | 디버그 모드 (전체 프롬프트 캡처) | `false` |

## 비용 추적

토큰 사용량 기반 비용 계산:

| 모델 | Input (1K tokens) | Output (1K tokens) |
|------|-------------------|-------------------|
| Claude Sonnet 4.5 | $0.003 | $0.015 |
| Claude Haiku | $0.00025 | $0.00125 |

## 트러블슈팅

### Phoenix 연결 실패

```
⚠️ Phoenix 연결 실패, 트레이싱 비활성화
```

- Phoenix 서버가 실행 중인지 확인
- `PHOENIX_ENDPOINT` 환경변수 확인
- 네트워크 연결 확인 (EKS의 경우 Service 이름)

### 트레이스가 보이지 않음

1. `TRACING_ENABLED=true` 확인
2. `TRACE_SAMPLE_RATE > 0` 확인
3. Phoenix UI에서 올바른 프로젝트 선택

## 참고 자료

- [Arize Phoenix 공식 문서](https://docs.arize.com/phoenix)
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/)
- [OpenInference](https://github.com/Arize-ai/openinference)
