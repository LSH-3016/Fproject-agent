# EKS 배포 가이드 (ap-northeast-2)

## 사전 준비사항

### 1. ECR 리포지토리 생성 (ap-northeast-2)
```bash
aws ecr create-repository \
  --repository-name diary-orchestrator-agent \
  --region ap-northeast-2
```

### 2. IAM Role 신뢰 관계 업데이트
DiaryOrchestratorAgentRole에 EKS 클러스터의 OIDC Provider 추가:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::324547056370:oidc-provider/oidc.eks.ap-northeast-2.amazonaws.com/id/YOUR_OIDC_ID"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.ap-northeast-2.amazonaws.com/id/YOUR_OIDC_ID:sub": "system:serviceaccount:default:diary-agent-sa"
        }
      }
    }
  ]
}
```

OIDC ID 확인:
```bash
aws eks describe-cluster --name eks-cluster --region ap-northeast-2 \
  --query "cluster.identity.oidc.issuer" --output text
```

### 3. IAM Role 권한 확인
DiaryOrchestratorAgentRole에 다음 권한이 있는지 확인:
- Bedrock 모델 호출 권한
- Secrets Manager 읽기 권한 (agent-secret)
- Knowledge Base 접근 권한

## 배포 순서

### 1. Docker 이미지 빌드 및 푸시
```bash
# ECR 로그인
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 324547056370.dkr.ecr.ap-northeast-2.amazonaws.com

# 이미지 빌드
docker build -t diary-orchestrator-agent .

# 태그 지정
docker tag diary-orchestrator-agent:latest 324547056370.dkr.ecr.ap-northeast-2.amazonaws.com/diary-orchestrator-agent:latest

# 푸시
docker push 324547056370.dkr.ecr.ap-northeast-2.amazonaws.com/diary-orchestrator-agent:latest
```

### 2. Kubernetes 리소스 배포
```bash
# Deployment 및 Service 배포
kubectl apply -f k8s/deployment.yaml

# Ingress 배포
kubectl apply -f k8s/ingress.yaml
```

### 3. 배포 확인
```bash
# Pod 상태 확인
kubectl get pods -l app=agent-api

# 로그 확인
kubectl logs -l app=agent-api --tail=100 -f

# Service 확인
kubectl get svc agent-api-service

# Ingress 확인
kubectl get ingress agent-api-ingress
kubectl describe ingress agent-api-ingress
```

## 주요 설정

### 리전: ap-northeast-2
- ECR 리포지토리
- AWS_REGION 환경변수
- Secrets Manager (agent-secret)
- ACM 인증서

### IRSA (IAM Roles for Service Accounts)
- ServiceAccount: `diary-agent-sa`
- IAM Role: `DiaryOrchestratorAgentRole`

### Karpenter
- NodeSelector: `karpenter.sh/nodepool: default`

## 트러블슈팅

### Pod가 시작되지 않는 경우
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Secrets Manager 접근 오류
- IAM Role의 신뢰 관계 확인
- ServiceAccount annotation 확인
- Secret이 ap-northeast-2에 존재하는지 확인

### Bedrock 접근 오류
- IAM Role에 Bedrock 권한 확인
- 모델 ARN이 올바른지 확인
- Knowledge Base ID가 올바른지 확인

## 업데이트
```bash
# 이미지 재빌드 및 푸시 후
kubectl rollout restart deployment agent-api-deployment
```

## 롤백
```bash
kubectl delete -f k8s/ingress.yaml
kubectl delete -f k8s/deployment.yaml
```

