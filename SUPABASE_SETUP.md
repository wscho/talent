# Supabase 설정 가이드

이 프로젝트는 Supabase를 백엔드 데이터베이스로 사용합니다.

## 1. Supabase 프로젝트 생성

1. [Supabase](https://supabase.com)에 가입 및 로그인
2. "New Project" 클릭
3. 프로젝트 이름, 데이터베이스 비밀번호, 리전 선택
4. 프로젝트 생성 완료 대기 (약 2분)

## 2. 테이블 생성

1. Supabase 대시보드에서 "SQL Editor" 메뉴 선택
2. `supabase_setup.sql` 파일의 내용을 복사하여 SQL Editor에 붙여넣기
3. "Run" 버튼 클릭하여 실행
4. 테이블이 성공적으로 생성되었는지 확인 (Table Editor에서 확인)

## 3. API 키 가져오기

1. Supabase 대시보드에서 "Settings" → "API Keys" 메뉴 선택
2. **Project URL** 찾기:
   - 페이지 상단의 주소창에서 확인 (예: `https://syawddnnabqwhkfucqtd.supabase.co`)
   - 또는 Settings → General 메뉴에서 확인
3. **API Key** 찾기 (두 가지 방법 중 하나 선택):

   **방법 1: Legacy 키 사용 (권장)**
   - "Legacy anon, service_role API keys" 탭 클릭
   - **anon public** 키를 복사 (예: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`)
   
   **방법 2: 새로운 Publishable 키 사용**
   - "Publishable and secret API keys" 탭에서
   - "Publishable key" 섹션의 키를 복사 (예: `sb_publishable_...`)
   - 또는 "Secret keys" 섹션의 키 사용 (서버 사이드용)

## 4. Streamlit Cloud 설정

### Streamlit Cloud Secrets 설정

1. Streamlit Cloud 대시보드에서 앱 선택
2. "Settings" → "Secrets" 클릭
3. 다음 형식으로 secrets 추가:

```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-anon-key-or-publishable-key"
```

### 로컬 개발 환경 설정

로컬에서 개발하는 경우 `.streamlit/secrets.toml` 파일 생성:

```bash
mkdir -p .streamlit
```

`.streamlit/secrets.toml` 파일 내용:

```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-anon-key-or-publishable-key"
```

⚠️ **주의**: `.streamlit/secrets.toml` 파일은 `.gitignore`에 추가하여 버전 관리에서 제외하세요.

## 5. 보안 설정 (선택사항)

기본적으로 모든 사용자가 읽기/쓰기가 가능하도록 설정되어 있습니다. 
프로덕션 환경에서는 RLS (Row Level Security) 정책을 수정하여 인증된 사용자만 접근하도록 설정하세요.

## 6. 구조

```
Streamlit Cloud (UI)
   ↓  HTTPS
Supabase (Backend)
   - PostgreSQL Database
   - REST API
   - Real-time subscriptions
```

## 문제 해결

- **연결 오류**: SUPABASE_URL과 SUPABASE_KEY가 올바른지 확인
- **테이블 없음**: SQL Editor에서 테이블 생성 스크립트 실행 확인
- **권한 오류**: RLS 정책 확인 및 수정
