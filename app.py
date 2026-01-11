import streamlit as st
import uuid
import pandas as pd
from datetime import datetime
from database import init_database, load_table, append_row, get_donors, get_requests, update_donor, update_request
from matching import calculate_match_score

# 데이터베이스 초기화
init_database()

st.set_page_config(
    page_title="재능기부포털",
    page_icon="🎁",
    layout="wide"
)

# 사이드바 정보
st.sidebar.title("📌 재능기부포털")

# Supabase 연결 확인
try:
    from database import get_supabase_client
    client = get_supabase_client()
    if client:
        st.sidebar.success("✅ Supabase 연결됨")
    else:
        st.sidebar.warning("⚠️ Supabase 설정 필요")
        with st.sidebar.expander("설정 방법"):
            st.markdown("""
            Streamlit Cloud Secrets에 다음을 추가하세요:
            ```toml
            SUPABASE_URL = "your-url"
            SUPABASE_KEY = "your-key"
            ```
            """)
except Exception as e:
    st.sidebar.error(f"❌ DB 연결 오류: {str(e)}")

# 메인 탭 구성
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🧑‍🤝‍🧑 재능기부자 등록",
    "🙋 재능수요자 등록",
    "👥 기부자 현황",
    "🙋 수요자 현황",
    "🔗 매칭 현황"
])

# ======================
# 탭1: 재능기부자 등록
# ======================
with tab1:
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
                    append_row("donors", {
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
# 탭2: 재능 수요자 등록
# ======================
with tab2:
    st.header("🙋 재능 수요자 등록")
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
                    append_row("requests", {
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
# 탭3: 기부자 현황
# ======================
with tab3:
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

                # 원본 데이터 준비 (donor_id 포함)
                display_columns = ["donor_id", "name", "email", "skill", "mode", "availability", "created_at"]
                display_df = donors[display_columns].copy()
                
                # 컬럼명 한글화
                display_df.columns = ["ID", "이름", "이메일", "재능", "방식", "가능 시간", "등록일시"]
                
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
                
                # 편집 가능한 데이터 표시 (ID와 등록일시는 편집 불가)
                edited_df = st.data_editor(
                    display_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "ID": st.column_config.TextColumn("ID", disabled=True),
                        "등록일시": st.column_config.TextColumn("등록일시", disabled=True)
                    },
                    num_rows="fixed"
                )
                
                # 변경사항 저장 버튼
                if st.button("💾 변경사항 저장", use_container_width=True, type="primary", key="save_donor_changes"):
                    try:
                        # 원본 데이터와 비교하여 변경된 행 찾기
                        original_df = display_df.copy()
                        
                        # 변경된 행 업데이트
                        updated_count = 0
                        for idx, row in edited_df.iterrows():
                            original_row = original_df.iloc[idx]
                            
                            # 변경사항 확인
                            if (row["이름"] != original_row["이름"] or
                                row["이메일"] != original_row["이메일"] or
                                row["재능"] != original_row["재능"] or
                                row["방식"] != original_row["방식"] or
                                row["가능 시간"] != original_row["가능 시간"]):
                                
                                update_donor(
                                    donor_id=row["ID"],
                                    name=row["이름"],
                                    email=row["이메일"],
                                    skill=row["재능"],
                                    mode=row["방식"],
                                    availability=row["가능 시간"] if pd.notna(row["가능 시간"]) else ""
                                )
                                updated_count += 1
                        
                        if updated_count > 0:
                            st.success(f"✅ {updated_count}개의 항목이 업데이트되었습니다!")
                            st.rerun()
                        else:
                            st.info("변경된 내용이 없습니다.")
                    except Exception as e:
                        st.error(f"❌ 저장 중 오류가 발생했습니다: {str(e)}")
                
                # 다운로드 버튼
                csv = edited_df.to_csv(index=False, encoding='utf-8-sig')
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
# 탭4: 수요자 현황
# ======================
with tab4:
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

                # 원본 데이터 준비 (request_id 포함)
                display_columns = ["request_id", "email", "needed_skill", "description", "status", "created_at"]
                display_df = requests[display_columns].copy()
                
                # 컬럼명 한글화
                display_df.columns = ["ID", "이메일", "필요한 재능", "요청 내용", "상태", "등록일시"]
                
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
                
                # 편집 가능한 데이터 표시 (ID와 등록일시는 편집 불가)
                edited_df = st.data_editor(
                    display_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "ID": st.column_config.TextColumn("ID", disabled=True),
                        "등록일시": st.column_config.TextColumn("등록일시", disabled=True),
                        "상태": st.column_config.SelectboxColumn(
                            "상태",
                            options=["대기", "처리 완료", "취소"]
                        )
                    },
                    num_rows="fixed"
                )
                
                # 변경사항 저장 버튼
                if st.button("💾 변경사항 저장", use_container_width=True, type="primary", key="save_request_changes"):
                    try:
                        # 원본 데이터와 비교하여 변경된 행 찾기
                        original_df = display_df.copy()
                        
                        # 변경된 행 업데이트
                        updated_count = 0
                        for idx, row in edited_df.iterrows():
                            original_row = original_df.iloc[idx]
                            
                            # 변경사항 확인
                            if (row["이메일"] != original_row["이메일"] or
                                row["필요한 재능"] != original_row["필요한 재능"] or
                                row["요청 내용"] != original_row["요청 내용"] or
                                row["상태"] != original_row["상태"]):
                                
                                update_request(
                                    request_id=row["ID"],
                                    email=row["이메일"],
                                    needed_skill=row["필요한 재능"],
                                    description=row["요청 내용"] if pd.notna(row["요청 내용"]) else "",
                                    status=row["상태"]
                                )
                                updated_count += 1
                        
                        if updated_count > 0:
                            st.success(f"✅ {updated_count}개의 항목이 업데이트되었습니다!")
                            st.rerun()
                        else:
                            st.info("변경된 내용이 없습니다.")
                    except Exception as e:
                        st.error(f"❌ 저장 중 오류가 발생했습니다: {str(e)}")
                
                # 다운로드 버튼
                csv = edited_df.to_csv(index=False, encoding='utf-8-sig')
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
# 탭5: 매칭 현황
# ======================
with tab5:
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
                
                # 매칭 옵션
                col1, col2 = st.columns(2)
                with col1:
                    match_status_filter = st.selectbox(
                        "수요자 상태 필터",
                        ["전체", "대기", "처리 완료"],
                        key="match_status_filter"
                    )
                with col2:
                    show_all_matches = st.checkbox("모든 매칭 표시 (상태 무관)", value=False, key="show_all_matches")

                matches = []

                # 모든 기부자와 수요자에 대해 wild 매칭 수행
                for _, r in requests.iterrows():
                    # 상태 필터 적용
                    if not show_all_matches:
                        if match_status_filter == "대기" and r.get("status", "대기") != "대기":
                            continue
                        elif match_status_filter == "처리 완료" and r.get("status", "대기") == "대기":
                            continue
                    
                    for _, d in donors.iterrows():
                        # wild 매칭 수행: 일부라도 일치하면 매칭
                        score = calculate_match_score(d["skill"], r["needed_skill"])
                        if score > 0:
                            matches.append({
                                "기부자 이름": d["name"],
                                "기부자 이메일": d["email"],
                                "기부자 재능": d["skill"],
                                "방식": d["mode"],
                                "가능 시간": d.get("availability", ""),
                                "수요자 이메일": r["email"],
                                "요청 재능": r["needed_skill"],
                                "요청 내용": r.get("description", ""),
                                "수요자 상태": r.get("status", "대기"),
                                "매칭 점수": score
                            })

                if matches:
                    # 매칭 결과를 DataFrame으로 변환
                    matches_df = pd.DataFrame(matches)
                    
                    # 정렬 옵션
                    sort_match_option = st.selectbox(
                        "정렬 기준",
                        ["매칭 점수 (높은순)", "기부자 이름", "수요자 이메일"],
                        key="sort_match_option"
                    )
                    
                    if sort_match_option == "매칭 점수 (높은순)":
                        matches_df = matches_df.sort_values("매칭 점수", ascending=False)
                    elif sort_match_option == "기부자 이름":
                        matches_df = matches_df.sort_values("기부자 이름", ascending=True)
                    elif sort_match_option == "수요자 이메일":
                        matches_df = matches_df.sort_values("수요자 이메일", ascending=True)
                    
                    st.dataframe(matches_df, use_container_width=True, hide_index=True)
                    
                    # 매칭 통계
                    st.markdown("---")
                    st.subheader("📈 매칭 통계")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("총 매칭 수", len(matches))
                    with col2:
                        unique_donors = matches_df["기부자 이메일"].nunique()
                        st.metric("매칭된 기부자", unique_donors)
                    with col3:
                        unique_requests = matches_df["수요자 이메일"].nunique()
                        st.metric("매칭된 수요자", unique_requests)
                    
                    # 다운로드 버튼
                    csv = matches_df.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label="📥 매칭 결과 CSV로 다운로드",
                        data=csv,
                        file_name=f"매칭_결과_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        key="download_matches"
                    )
                else:
                    st.info("현재 매칭 가능한 항목이 없습니다. 재능 키워드를 확인해주세요.")

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
3. **현황**: 기부자, 수요자, 매칭 현황을 확인하세요
""")

