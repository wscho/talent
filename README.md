# 🎁 재능기부 매칭 플랫폼

Supabase와 Streamlit을 기반으로 한 재능기부 매칭 시스템입니다.
재능기부자가 앱에서 자신이 보유한 기술을 등록하고, 재능수요자가 필요한 기술을 등록하면 자동으로 매칭됩니다. 

## ✨ 특징

- ✅ 클라우드 기반 데이터베이스 (Supabase)
- ✅ Streamlit Cloud로 간편한 배포
- ✅ 실시간 데이터 동기화
- ✅ 확장 가능한 구조
- ✅ HTTPS 자동 지원

## 📋 사전 요구사항

1. Python 3.7 이상
2. Supabase 계정 (무료 플랜 가능)
3. Streamlit Cloud 계정 (선택사항, 배포 시)

## 🚀 빠른 시작

### 1. Supabase 설정

1. [Supabase](https://supabase.com)에 가입 및 로그인
2. 새 프로젝트 생성
3. `supabase_setup.sql` 파일을 SQL Editor에서 실행하여 테이블 생성
4. Settings → API Keys에서 Project URL과 API Key 복사

자세한 설정 방법은 [SUPABASE_SETUP.md](SUPABASE_SETUP.md) 파일을 참고하세요.

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 로컬 개발 환경 설정

`.streamlit/secrets.toml` 파일 생성:

```bash
# Windows (PowerShell)
mkdir .streamlit
```

`.streamlit/secrets.toml` 파일 내용:

```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-anon-key-here"
```

⚠️ **주의**: `.streamlit/secrets.toml` 파일은 Git에 커밋하지 마세요 (이미 `.gitignore`에 포함됨)

### 4. 로컬에서 실행

```bash
streamlit run app.py
```

브라우저에서 자동으로 열리며, 다음 기능을 사용할 수 있습니다:

- 🧑‍🤝‍🧑 **재능기부자 등록**: 자신의 재능을 등록
- 🙋 **재능수요자 등록**: 필요한 재능을 요청
- 👥 **기부자 현황**: 등록된 기부자 목록 및 편집
- 🙋 **수요자 현황**: 등록된 수요자 목록 및 편집
- 🔗 **매칭 현황**: Wild 매칭을 통한 자동 매칭 결과

## ☁️ Streamlit Cloud 배포

### 1. GitHub에 코드 푸시

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/talent.git
git push -u origin main
```

### 2. Streamlit Cloud 연결

1. [Streamlit Cloud](https://streamlit.io/cloud)에 로그인
2. "New app" 클릭
3. GitHub 저장소 선택
4. Branch: `main`, Main file: `app.py` 선택
5. "Advanced settings" → "Secrets"에서 다음 추가:

```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-anon-key-here"
```

6. "Deploy" 클릭

배포가 완료되면 자동으로 HTTPS URL이 생성됩니다!

## 📁 프로젝트 구조

```
talent/
 ├─ app.py                 # Streamlit 메인 앱
 ├─ database.py            # Supabase 데이터베이스 연동 모듈
 ├─ matching.py            # Wild 매칭 로직
 ├─ requirements.txt       # 의존성 목록
 ├─ supabase_setup.sql     # Supabase 테이블 생성 SQL
 ├─ SUPABASE_SETUP.md      # Supabase 설정 가이드
 └─ README.md              # 프로젝트 설명
```

## 🗄️ 데이터베이스 구조

### Donors 테이블
```
donor_id | name | email | skill | mode | availability | created_at
```

### Requests 테이블
```
request_id | email | needed_skill | description | status | created_at
```

### Matches 테이블
```
match_id | donor_id | request_id | score | status | created_at
```

## 🔧 주요 기능

### 재능기부자 등록
- 이름/닉네임, 이메일, 재능, 방식(온라인/오프라인), 가능 시간 입력
- Supabase 데이터베이스의 `Donors` 테이블에 자동 저장

### 재능수요자 등록
- 이메일, 필요한 재능, 요청 내용 입력
- Supabase 데이터베이스의 `Requests` 테이블에 자동 저장

### 기부자/수요자 현황
- 등록된 데이터 목록 확인
- 셀 편집 기능으로 직접 수정 가능
- 검색, 정렬, 필터 기능
- CSV 다운로드 지원

### 매칭 현황
- Wild 매칭 알고리즘으로 자동 매칭
- 재능 키워드 부분 일치 기반 매칭
- 매칭 통계 및 결과 다운로드

## 🌐 아키텍처

```
Streamlit Cloud (UI)
   ↓  HTTPS
Supabase (Backend)
   - PostgreSQL Database
   - REST API
   - Real-time subscriptions
```

## 🔐 보안

- Streamlit Secrets를 통한 안전한 키 관리
- Supabase RLS (Row Level Security) 지원
- HTTPS 자동 적용 (Streamlit Cloud)

## 📝 라이선스

이 프로젝트는 자유롭게 사용 가능합니다.
