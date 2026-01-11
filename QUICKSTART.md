# 🚀 빠른 실행 가이드

## 로컬에서 실행하기

### 1단계: Supabase 설정 (5분)

1. [Supabase](https://supabase.com) 접속 → "Start your project" → "New Project"
2. 프로젝트 이름 입력 → 데이터베이스 비밀번호 설정 → 리전 선택 → "Create new project"
3. 프로젝트 생성 완료 대기 (약 2분)
4. 좌측 메뉴 "SQL Editor" 클릭
5. `supabase_setup.sql` 파일의 내용을 복사하여 붙여넣기 → "Run" 버튼 클릭
6. 좌측 메뉴 "Settings" → "API Keys" 클릭
7. "Legacy anon, service_role API keys" 탭 클릭
8. **anon public** 키 복사 (복사 아이콘 클릭)
9. 브라우저 주소창에서 **Project URL** 확인 (예: `https://xxxxxxxxxxxxx.supabase.co`)

### 2단계: 로컬 환경 설정 (2분)

1. 프로젝트 폴더에서 의존성 설치:
```bash
pip install -r requirements.txt
```

2. `.streamlit/secrets.toml` 파일 생성:
```bash
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path .streamlit
New-Item -ItemType File -Path .streamlit\secrets.toml
```

3. `.streamlit/secrets.toml` 파일에 다음 내용 입력:
```toml
SUPABASE_URL = "여기에_Project_URL_붙여넣기"
SUPABASE_KEY = "여기에_anon_public_키_붙여넣기"
```

예시:
```toml
SUPABASE_URL = "https://syawddnnabqwhkfucqtd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN5YXdkZG5uYWJxd2hrZnVjcXRkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MT..."
```

### 3단계: 실행 (1분)

```bash
streamlit run app.py
```

브라우저가 자동으로 열리면 완료! 🎉

## Streamlit Cloud에 배포하기

### 1단계: GitHub에 코드 푸시

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/talent.git
git push -u origin main
```

### 2단계: Streamlit Cloud 설정

1. [Streamlit Cloud](https://streamlit.io/cloud) 접속 → GitHub로 로그인
2. "New app" 클릭
3. Repository: `yourusername/talent` 선택
4. Branch: `main` 선택
5. Main file path: `app.py` 선택
6. "Advanced settings" 클릭 → "Secrets" 섹션에 다음 추가:
```toml
SUPABASE_URL = "여기에_Project_URL_붙여넣기"
SUPABASE_KEY = "여기에_anon_public_키_붙여넣기"
```
7. "Save" → "Deploy!" 클릭

배포 완료 후 생성된 URL로 접속 가능합니다! 🚀

## 문제 해결

### ❌ "Supabase 설정 필요" 메시지가 나타나는 경우
- `.streamlit/secrets.toml` 파일이 올바른 위치에 있는지 확인
- SUPABASE_URL과 SUPABASE_KEY가 올바르게 입력되었는지 확인
- 키에 따옴표가 없는지 확인

### ❌ "테이블 조회 오류"가 발생하는 경우
- Supabase SQL Editor에서 `supabase_setup.sql`이 정상 실행되었는지 확인
- Supabase Table Editor에서 Donors, Requests, Matches 테이블이 생성되었는지 확인

### ❌ 연결 오류가 발생하는 경우
- 인터넷 연결 확인
- Supabase 프로젝트가 활성 상태인지 확인
- API 키가 올바른지 확인 (anon public 키 사용)

더 자세한 내용은 [SUPABASE_SETUP.md](SUPABASE_SETUP.md)를 참고하세요.
