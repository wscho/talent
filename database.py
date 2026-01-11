import pandas as pd
from supabase import create_client, Client
import streamlit as st
from typing import Optional

def get_supabase_client() -> Optional[Client]:
    """Supabase 클라이언트 생성"""
    try:
        # Streamlit secrets에서 Supabase 설정 가져오기
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        
        if not url or not key:
            return None
        
        # URL이 기본값인지 확인
        if "your-project-id" in url or "your-anon-key" in key:
            return None
        
        return create_client(url, key)
    except (KeyError, AttributeError):
        # secrets에 키가 없거나 secrets가 없는 경우
        return None
    except Exception:
        # 기타 오류
        return None

def init_database():
    """데이터베이스 초기화 (Supabase는 이미 생성되어 있어야 함)"""
    # Supabase는 클라우드 데이터베이스이므로 여기서는 연결만 확인
    client = get_supabase_client()
    if client:
        return True
    return False

def load_table(table_name: str) -> pd.DataFrame:
    """테이블 데이터를 DataFrame으로 로드"""
    # 설정 확인
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        
        # 기본값 확인
        if "your-project-id" in url or "your-anon-key" in key or not url or not key:
            st.error("⚠️ Supabase 설정이 필요합니다!\n\n.streamlit/secrets.toml 파일에 실제 Supabase 정보를 입력해주세요.\n\n설정 방법은 SUPABASE_SETUP.md 파일을 참고하세요.")
            return pd.DataFrame()
    except (KeyError, AttributeError):
        st.error("⚠️ Supabase 설정이 필요합니다!\n\n.streamlit/secrets.toml 파일에 SUPABASE_URL과 SUPABASE_KEY를 설정해주세요.")
        return pd.DataFrame()
    
    client = get_supabase_client()
    if not client:
        st.error("⚠️ Supabase 클라이언트를 생성할 수 없습니다!\n\n.streamlit/secrets.toml 파일의 SUPABASE_URL과 SUPABASE_KEY를 확인해주세요.")
        return pd.DataFrame()
    
    try:
        response = client.table(table_name).select("*").execute()
        if response.data:
            return pd.DataFrame(response.data)
        else:
            return pd.DataFrame()
    except Exception as e:
        error_msg = str(e)
        if "getaddrinfo failed" in error_msg.lower() or "failed to resolve" in error_msg.lower():
            try:
                url = st.secrets["SUPABASE_URL"]
                st.error(f"⚠️ Supabase 서버에 연결할 수 없습니다!\n\n원인:\n- SUPABASE_URL이 올바르지 않을 수 있습니다 (현재: {url[:60] if len(url) > 60 else url})\n- 인터넷 연결을 확인해주세요\n- Supabase 프로젝트가 활성 상태인지 확인해주세요\n\n설정 확인:\n1. Supabase 대시보드 → Settings → API Keys\n2. 브라우저 주소창에서 Project URL 확인\n3. .streamlit/secrets.toml 파일에 올바른 URL 입력")
            except:
                st.error(f"⚠️ Supabase 서버에 연결할 수 없습니다!\n\n.streamlit/secrets.toml 파일의 SUPABASE_URL을 확인해주세요.")
        elif "JWT" in error_msg or "unauthorized" in error_msg.lower() or "401" in error_msg:
            st.error(f"⚠️ 인증 오류가 발생했습니다!\n\nSUPABASE_KEY가 올바른지 확인해주세요:\n- Settings → API Keys → Legacy anon, service_role API keys\n- anon public 키를 복사하여 사용")
        else:
            st.error(f"❌ 테이블 조회 오류 ({table_name}): {error_msg}")
        return pd.DataFrame()

def append_row(table_name: str, row_data: dict):
    """테이블에 행 추가
    
    Args:
        table_name: 테이블 이름 (Donors, Requests, Matches)
        row_data: 딕셔너리 형태의 데이터
    """
    # 설정 확인
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        
        # 기본값 확인
        if "your-project-id" in url or "your-anon-key" in key or not url or not key:
            raise Exception("⚠️ Supabase 설정이 필요합니다!\n\n.streamlit/secrets.toml 파일에 실제 Supabase 정보를 입력해주세요:\n- SUPABASE_URL: Supabase 프로젝트 URL\n- SUPABASE_KEY: anon public 키\n\n설정 방법은 SUPABASE_SETUP.md 파일을 참고하세요.")
    except (KeyError, AttributeError):
        raise Exception("⚠️ Supabase 설정이 필요합니다!\n\n.streamlit/secrets.toml 파일에 SUPABASE_URL과 SUPABASE_KEY를 설정해주세요.\n\n설정 방법은 SUPABASE_SETUP.md 파일을 참고하세요.")
    
    client = get_supabase_client()
    if not client:
        raise Exception("⚠️ Supabase 클라이언트를 생성할 수 없습니다!\n\n.streamlit/secrets.toml 파일의 SUPABASE_URL과 SUPABASE_KEY를 확인해주세요.\n- SUPABASE_URL이 올바른 형식인지 확인 (예: https://xxxxx.supabase.co)\n- SUPABASE_KEY가 올바른 anon public 키인지 확인")
    
    try:
        response = client.table(table_name).insert(row_data).execute()
        return response.data
    except Exception as e:
        error_msg = str(e)
        if "getaddrinfo failed" in error_msg.lower() or "failed to resolve" in error_msg.lower():
            raise Exception(f"⚠️ Supabase 서버에 연결할 수 없습니다!\n\n원인:\n- SUPABASE_URL이 올바르지 않을 수 있습니다 (현재: {url[:60] if len(url) > 60 else url})\n- 인터넷 연결을 확인해주세요\n- Supabase 프로젝트가 활성 상태인지 확인해주세요\n\n설정 확인:\n1. Supabase 대시보드 → Settings → API Keys\n2. 브라우저 주소창에서 Project URL 확인\n3. .streamlit/secrets.toml 파일에 올바른 URL 입력")
        elif "duplicate key" in error_msg.lower() or "unique constraint" in error_msg.lower():
            raise Exception(f"이미 존재하는 데이터입니다: {error_msg}")
        elif "JWT" in error_msg or "unauthorized" in error_msg.lower() or "401" in error_msg:
            raise Exception(f"⚠️ 인증 오류가 발생했습니다!\n\nSUPABASE_KEY가 올바른지 확인해주세요:\n- Settings → API Keys → Legacy anon, service_role API keys\n- anon public 키를 복사하여 사용\n\n오류 상세: {error_msg}")
        else:
            raise Exception(f"데이터 추가 오류: {error_msg}")

def get_donors() -> pd.DataFrame:
    """모든 재능기부자 조회"""
    return load_table("donors")

def get_requests() -> pd.DataFrame:
    """모든 재능 수요 조회"""
    return load_table("requests")

def get_matches() -> pd.DataFrame:
    """모든 매칭 조회"""
    return load_table("matches")

def update_donor(donor_id: str, name: str, email: str, skill: str, mode: str, availability: str):
    """재능기부자 정보 업데이트"""
    client = get_supabase_client()
    if not client:
        raise Exception("Supabase 클라이언트를 생성할 수 없습니다.")
    
    try:
        update_data = {
            "name": name,
            "email": email,
            "skill": skill,
            "mode": mode,
            "availability": availability
        }
        response = client.table("donors").update(update_data).eq("donor_id", donor_id).execute()
        return response.data
    except Exception as e:
        raise Exception(f"데이터 업데이트 오류: {str(e)}")

def update_request(request_id: str, email: str, needed_skill: str, description: str, status: str):
    """재능 수요 정보 업데이트"""
    client = get_supabase_client()
    if not client:
        raise Exception("Supabase 클라이언트를 생성할 수 없습니다.")
    
    try:
        update_data = {
            "email": email,
            "needed_skill": needed_skill,
            "description": description,
            "status": status
        }
        response = client.table("requests").update(update_data).eq("request_id", request_id).execute()
        return response.data
    except Exception as e:
        raise Exception(f"데이터 업데이트 오류: {str(e)}")
