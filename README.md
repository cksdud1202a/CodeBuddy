# CodeBuddy Agent

AWS Bedrock 기반 GitHub PR 자동 리뷰 AI Agent

## 아키텍처

```
GitHub PR → Bedrock Agent (CodeBuddy) → Lambda Tools → GitHub API
                    ↓
             Knowledge Base (PEP8, OWASP)
```

## 구성 요소

| 구성 요소 | 설명 |
|-----------|------|
| Bedrock Agent | CodeBuddy-Reviewer (Claude 3.5 Sonnet) |
| Knowledge Base | 코드 스타일/보안 가이드 문서 |
| Lambda: codebuddy-github-pr | GitHub PR 정보 및 diff 조회 |
| Lambda: codebuddy-list-repos | GitHub 저장소 목록 조회 |

## 기능

- **PR 코드 리뷰**: GitHub PR의 변경 코드를 분석하여 버그, 보안 취약점, 스타일 위반 탐지
- **저장소 목록 조회**: GitHub 사용자/조직의 저장소 목록 조회
- **심각도 분류**:
  - 🔴 높은 심각도: 보안 취약점, 버그
  - 🟡 중간 심각도: 코드 품질 개선 사항
  - 🟢 낮은 심각도: 스타일 권장사항

## 사용 방법

### PR 리뷰 요청

```python
invoke_agent("cksdud1202a/kt-cloud-basic 저장소의 PR #1 코드를 리뷰해줘")
```

### 저장소 목록 조회

```python
invoke_agent("cksdud1202a의 GitHub 저장소 목록을 보여줘")
```

## 환경 설정

### Colab Secrets 설정

| Secret | 설명 |
|--------|------|
| AWS_ACCESS_KEY_ID | AWS 액세스 키 |
| AWS_SECRET_ACCESS_KEY | AWS 시크릿 키 |
| GITHUB_TOKEN | GitHub Personal Access Token |
| AGENT_ID | Bedrock Agent ID |
| AGENT_ALIAS_ID | Bedrock Agent Alias ID |
| KB_ID | Knowledge Base ID |

### 실행

1. `notebook/codebuddy.ipynb`를 Google Colab에서 열기
2. Colab Secrets에 위 환경변수 설정
3. 셀 순서대로 실행

## Lambda 함수

### codebuddy-github-pr

GitHub PR 정보 및 코드 diff를 조회합니다.

**파라미터**
- `owner`: 저장소 소유자
- `repo`: 저장소 이름
- `pr_number`: PR 번호

### codebuddy-list-repos

GitHub 사용자/조직의 저장소 목록을 조회합니다.

**파라미터**
- `owner`: GitHub 사용자명 또는 조직명
- `type`: 저장소 유형 (all/public/private, 선택사항)

## 비용 (서울 리전, 하루 100회 기준)

| 서비스 | 월 예상 비용 |
|--------|-------------|
| Lambda | $11.00 |
| Bedrock (Claude 3.5 Sonnet) | $4.40 |
| Knowledge Base | $11.00 |
| 합계 | ~$27.79 |
