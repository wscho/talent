import streamlit as st
import uuid
import pandas as pd
from datetime import datetime
from database import init_database, load_table, append_row, get_donors, get_requests
from matching import calculate_match_score

# 데이터베이스 초기화
init_database()

st.set_page_config(
    page_title="재능기부 매칭 플랫폼",
    page_icon="🎁",
    layout="wide"
)

# 사이드바 메뉴
st.sidebar.title("📌 재능기부 매칭 플랫폼")
st.sidebar.success("✅ SQLite 데이터베이스 연결됨")

menu = st.sidebar.selectbox(
    "메뉴 선택",
    ["재능기부자 등록", "재능수요자 등록", "기부자 현황", "수요자 현황", "매칭 현황"]
)

# ======================
# 재능기부자 등록
# ======================
if menu == "재능기부자 등록":
    st.header("🧑‍🤝‍🧑 재능기부자 등록")
    st.markdown("---")

    with st.form("donor_form"):
        name = st.text_input("이름/닉네임 *", placeholder="홍길동")
        email = st.text_input("이메일 *", placeholder="example@email.com")
        skill = st.text_input("재능 *", placeholder="파이썬, 수학, 영어")
        mode = st.selectbox("방식 *", ["온라인", "오프라인", "온라인/오프라인"])
        availability = st.text_input("가능 시간", placeholder="주말 오후 2시~5시")

        submitted = st.form_submit_button("등록하기", use_container_width=True)

        if submitted:
            if not name or not email or not skill:
                st.error("필수 항목(이름, 이메일, 재능)을 모두 입력해주세요.")
            else:
                try:
                    append_row("Donors", {
                        "donor_id": str(uuid.uuid4()),
                        "name": name,
                        "email": email,
                        "skill": skill,
                        "mode": mode,
                        "availability": availability if availability else "",
                        "created_at": datetime.now().isoformat()
                    })
                    st.success("✅ 재능기부자로 등록되었습니다!")
                    st.balloons()
                except Exception as e:
                    error_msg = str(e)
                    st.error(f"❌ 등록 중 오류가 발생했습니다: {error_msg}")
                    st.info("💡 문제가 계속되면 README.md 파일을 참고하세요.")

# ======================
# 재능 수요자 등록
# ======================
elif menu == "재능수요자 등록":
    st.header("🙋 재능이 필요한 사람 등록")
    st.markdown("---")

    with st.form("request_form"):
        email = st.text_input("이메일 *", placeholder="example@email.com")
        needed_skill = st.text_input("필요한 재능 *", placeholder="파이썬 프로그래밍")
        desc = st.text_area("요청 내용", placeholder="파이썬 기초부터 배우고 싶습니다...")

        submitted = st.form_submit_button("등록하기", use_container_width=True)

        if submitted:
            if not email or not needed_skill:
                st.error("필수 항목(이메일, 필요한 재능)을 모두 입력해주세요.")
            else:
                try:
                    append_row("Requests", {
                        "request_id": str(uuid.uuid4()),
                        "email": email,
                        "needed_skill": needed_skill,
                        "description": desc if desc else "",
                        "status": "대기",
                        "created_at": datetime.now().isoformat()
                    })
                    st.success("✅ 요청이 등록되었습니다!")
                    st.balloons()
                except Exception as e:
                    error_msg = str(e)
                    st.error(f"❌ 등록 중 오류가 발생했습니다: {error_msg}")
                    st.info("💡 문제가 계속되면 README.md 파일을 참고하세요.")

# ======================
# 기부자 현황
# ======================
elif menu == "기부자 현황":
    st.header("👥 기부자 현황")
    st.markdown("---")

    try:
        donors = get_donors()

        if donors.empty:
            st.warning("등록된 재능기부자가 없습니다.")
        else:
            # 통계 정보
            st.subheader("📊 통계")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("총 기부자 수", len(donors))
            with col2:
                online_count = len(donors[donors["mode"].str.contains("온라인", na=False)])
                st.metric("온라인 가능", online_count)
            with col3:
                offline_count = len(donors[donors["mode"].str.contains("오프라인", na=False)])
                st.metric("오프라인 가능", offline_count)

            st.markdown("---")
            st.subheader("📋 기부자 목록")

            # 표시할 컬럼 선택
            display_columns = ["name", "email", "skill", "mode", "availability", "created_at"]
            display_df = donors[display_columns].copy()
            
            # 컬럼명 한글화
            display_df.columns = ["이름", "이메일", "재능", "방식", "가능 시간", "등록일시"]
            
            # 날짜 포맷팅
            if not display_df.empty:
                display_df["등록일시"] = pd.to_datetime(display_df["등록일시"]).dt.strftime("%Y-%m-%d %H:%M")
            
            # 검색 기능
            search_term = st.text_input("🔍 검색 (이름, 이메일, 재능으로 검색)", "")
            
            if search_term:
                mask = (
                    display_df["이름"].str.contains(search_term, case=False, na=False) |
                    display_df["이메일"].str.contains(search_term, case=False, na=False) |
                    display_df["재능"].str.contains(search_term, case=False, na=False)
                )
                display_df = display_df[mask]
            
            # 정렬 옵션
            sort_option = st.selectbox("정렬 기준", ["등록일시 (최신순)", "등록일시 (오래된순)", "이름 (가나다순)"])
            if sort_option == "등록일시 (최신순)":
                display_df = display_df.sort_values("등록일시", ascending=False)
            elif sort_option == "등록일시 (오래된순)":
                display_df = display_df.sort_values("등록일시", ascending=True)
            elif sort_option == "이름 (가나다순)":
                display_df = display_df.sort_values("이름", ascending=True)
            
            # 데이터 표시
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # 다운로드 버튼
            csv = display_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 CSV로 다운로드",
                data=csv,
                file_name=f"기부자_현황_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

    except Exception as e:
        error_msg = str(e)
        st.error(f"❌ 데이터를 불러오는 중 오류가 발생했습니다: {error_msg}")
        st.info("💡 문제가 계속되면 README.md 파일을 참고하세요.")

# ======================
# 수요자 현황
# ======================
elif menu == "수요자 현황":
    st.header("🙋 수요자 현황")
    st.markdown("---")

    try:
        requests = get_requests()

        if requests.empty:
            st.warning("등록된 재능 수요가 없습니다.")
        else:
            # 통계 정보
            st.subheader("📊 통계")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("총 수요 수", len(requests))
            with col2:
                waiting_count = len(requests[requests["status"] == "대기"])
                st.metric("대기 중", waiting_count)
            with col3:
                completed_count = len(requests[requests["status"] != "대기"])
                st.metric("처리 완료", completed_count)

            st.markdown("---")
            st.subheader("📋 수요자 목록")

            # 표시할 컬럼 선택
            display_columns = ["email", "needed_skill", "description", "status", "created_at"]
            display_df = requests[display_columns].copy()
            
            # 컬럼명 한글화
            display_df.columns = ["이메일", "필요한 재능", "요청 내용", "상태", "등록일시"]
            
            # 날짜 포맷팅
            if not display_df.empty:
                display_df["등록일시"] = pd.to_datetime(display_df["등록일시"]).dt.strftime("%Y-%m-%d %H:%M")
            
            # 상태별 필터
            status_filter = st.selectbox("상태 필터", ["전체", "대기", "처리 완료"])
            if status_filter == "대기":
                display_df = display_df[display_df["상태"] == "대기"]
            elif status_filter == "처리 완료":
                display_df = display_df[display_df["상태"] != "대기"]
            
            # 검색 기능
            search_term = st.text_input("🔍 검색 (이메일, 필요한 재능으로 검색)", "")
            
            if search_term:
                mask = (
                    display_df["이메일"].str.contains(search_term, case=False, na=False) |
                    display_df["필요한 재능"].str.contains(search_term, case=False, na=False)
                )
                display_df = display_df[mask]
            
            # 정렬 옵션
            sort_option = st.selectbox("정렬 기준", ["등록일시 (최신순)", "등록일시 (오래된순)", "상태"])
            if sort_option == "등록일시 (최신순)":
                display_df = display_df.sort_values("등록일시", ascending=False)
            elif sort_option == "등록일시 (오래된순)":
                display_df = display_df.sort_values("등록일시", ascending=True)
            elif sort_option == "상태":
                display_df = display_df.sort_values("상태", ascending=True)
            
            # 데이터 표시
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # 다운로드 버튼
            csv = display_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 CSV로 다운로드",
                data=csv,
                file_name=f"수요자_현황_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

    except Exception as e:
        error_msg = str(e)
        st.error(f"❌ 데이터를 불러오는 중 오류가 발생했습니다: {error_msg}")
        st.info("💡 문제가 계속되면 README.md 파일을 참고하세요.")

# ======================
# 매칭 현황
# ======================
elif menu == "매칭 현황":
    st.header("🔗 매칭 현황")
    st.markdown("---")

    try:
        donors = get_donors()
        requests = get_requests()

        if donors.empty:
            st.warning("등록된 재능기부자가 없습니다.")
        elif requests.empty:
            st.warning("등록된 재능 수요가 없습니다.")
        else:
            st.subheader("📊 등록 현황")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("재능기부자 수", len(donors))
            with col2:
                st.metric("재능 수요 수", len(requests))

            st.markdown("---")
            st.subheader("🎯 매칭 결과")

            matches = []

            for _, r in requests.iterrows():
                if r.get("status", "대기") != "대기":
                    continue
                for _, d in donors.iterrows():
                    score = calculate_match_score(d["skill"], r["needed_skill"])
                    if score > 0:
                        matches.append({
                            "기부자 이름": d["name"],
                            "기부자 이메일": d["email"],
                            "기부자 재능": d["skill"],
                            "방식": d["mode"],
                            "수요자 이메일": r["email"],
                            "요청 재능": r["needed_skill"],
                            "요청 내용": r.get("description", ""),
                            "매칭 점수": score
                        })

            if matches:
                st.dataframe(matches, use_container_width=True)
                
                # 매칭 통계
                st.markdown("---")
                st.subheader("📈 매칭 통계")
                st.info(f"총 {len(matches)}개의 매칭이 발견되었습니다.")
            else:
                st.info("현재 매칭 가능한 항목이 없습니다.")

    except Exception as e:
        error_msg = str(e)
        st.error(f"❌ 데이터를 불러오는 중 오류가 발생했습니다: {error_msg}")
        st.info("💡 문제가 계속되면 README.md 파일을 참고하세요.")

# 사이드바 하단 정보
st.sidebar.markdown("---")
st.sidebar.markdown("""
### ℹ️ 사용 방법
1. **재능기부자 등록**: 자신의 재능을 등록하세요
2. **재능수요자 등록**: 필요한 재능을 요청하세요
3. **기부자 현황**: 등록된 모든 기부자 목록을 확인하세요
4. **수요자 현황**: 등록된 모든 수요자 목록을 확인하세요
5. **매칭 현황**: 등록된 정보를 기반으로 매칭 결과를 확인하세요
""")

