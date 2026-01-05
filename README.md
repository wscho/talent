# 🎁 재능기부 매칭 플랫폼

SQLite와 Streamlit을 기반으로 한 경량 재능기부 매칭 시스템입니다.

## ✨ 특징

- ✅ 서버 불필요
- ✅ 외부 서비스 불필요 (Google Sheet 등)
- ✅ 배포 간단
- ✅ 유지비 0원
- ✅ SQLite를 단일 데이터 소스로 사용
- ✅ 로컬 파일 기반 데이터베이스

## 📋 사전 요구사항

1. Python 3.7 이상
2. 추가 설정 불필요 (SQLite는 Python 표준 라이브러리)

## 🚀 설치 방법

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 데이터베이스 초기화

앱을 처음 실행하면 자동으로 `talent_matching.db` 파일이 생성되고 필요한 테이블이 생성됩니다.

## 🎯 실행 방법

```bash
streamlit run app.py
```

브라우저에서 자동으로 열리며, 다음 기능을 사용할 수 있습니다:

- 🧑‍🤝‍🧑 **재능기부자 등록**: 자신의 재능을 등록
- 🙋 **재능수요자 등록**: 필요한 재능을 요청
- 🔗 **매칭 현황**: 등록된 정보를 기반으로 매칭 결과 확인

## 📁 프로젝트 구조

```
talent_matching/
 ├─ app.py                 # Streamlit 메인 앱
 ├─ database.py            # SQLite 데이터베이스 연동 모듈
 ├─ matching.py            # 매칭 로직
 ├─ talent_matching.db     # SQLite 데이터베이스 파일 (자동 생성)
 ├─ requirements.txt       # 의존성 목록
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
- SQLite 데이터베이스의 `Donors` 테이블에 자동 저장

### 재능수요자 등록
- 이메일, 필요한 재능, 요청 내용 입력
- SQLite 데이터베이스의 `Requests` 테이블에 자동 저장

### 매칭 현황
- 등록된 재능기부자와 수요자를 자동 매칭
- 매칭 점수 기반으로 결과 표시
- 등록 현황 통계 제공

## 💾 데이터 관리

### 데이터베이스 파일 위치
- 데이터베이스 파일: `talent_matching.db` (프로젝트 루트 디렉토리)
- 앱을 처음 실행하면 자동으로 생성됩니다

### 데이터 백업
데이터베이스 파일(`talent_matching.db`)을 정기적으로 백업하세요:
```bash
# Windows
copy talent_matching.db talent_matching_backup.db

# Linux/Mac
cp talent_matching.db talent_matching_backup.db
```

### 데이터 초기화
데이터베이스를 초기화하려면 `talent_matching.db` 파일을 삭제하고 앱을 다시 실행하세요.

## ⚠️ 주의사항

- `talent_matching.db` 파일은 데이터베이스이므로 삭제하지 마세요
- 데이터베이스 파일을 정기적으로 백업하세요
- 동시 사용자 수가 많으면 성능이 저하될 수 있습니다 (SQLite의 한계)
- 대용량 데이터에는 적합하지 않습니다

## 🔄 Google Sheet에서 SQLite로 마이그레이션

이전에 Google Sheet를 사용하던 경우:

1. Google Sheet에서 데이터를 CSV로 내보내기
2. SQLite 데이터베이스에 데이터 임포트
3. 또는 앱을 새로 시작하여 데이터를 다시 등록

## 📝 라이선스

이 프로젝트는 자유롭게 사용 가능합니다.
