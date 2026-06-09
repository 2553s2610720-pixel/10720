import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="아침 조례 출결 확인",
    page_icon="📋",
    layout="wide"
)

# ---------------------------
# 초기 데이터
# ---------------------------
STUDENTS = [
    "김민준",
    "이서준",
    "박도윤",
    "최예은",
    "정하린",
    "윤지우",
    "강시우",
    "한지민",
    "오수빈",
    "신현우"
]

if "attendance" not in st.session_state:
    st.session_state.attendance = {
        student: "출석"
        for student in STUDENTS
    }

# ---------------------------
# 제목
# ---------------------------
st.title("📋 아침 조례 출결 확인 시스템")
st.caption("담임교사용 간단 출결 관리 앱")

# ---------------------------
# 출결 입력
# ---------------------------
st.subheader("✏️ 출결 입력 및 수정")

col1, col2 = st.columns([2, 1])

with col1:
    for student in STUDENTS:
        st.session_state.attendance[student] = st.selectbox(
            f"{student}",
            ["출석", "지각", "결석"],
            index=["출석", "지각", "결석"].index(
                st.session_state.attendance[student]
            ),
            key=student
        )

# ---------------------------
# 데이터 생성
# ---------------------------
df = pd.DataFrame({
    "학생명": list(st.session_state.attendance.keys()),
    "상태": list(st.session_state.attendance.values())
})

present_count = len(df[df["상태"] == "출석"])
late_count = len(df[df["상태"] == "지각"])
absent_count = len(df[df["상태"] == "결석"])

attendance_rate = (
    (present_count + late_count) / len(df) * 100
)

# ---------------------------
# 통계
# ---------------------------
with col2:
    st.subheader("📊 오늘의 통계")

    st.metric("출석", present_count)
    st.metric("지각", late_count)
    st.metric("결석", absent_count)
    st.metric("출석률", f"{attendance_rate:.1f}%")

# ---------------------------
# 알림
# ---------------------------
absent_students = df[df["상태"] == "결석"]["학생명"].tolist()

st.divider()

if absent_students:
    st.error(
        f"🚨 담임교사 알림: 결석 학생 {len(absent_students)}명 발생"
    )

    st.warning(
        "결석 학생: " + ", ".join(absent_students)
    )

    with st.sidebar:
        st.error("결석 학생 발생")
        for student in absent_students:
            st.write(f"• {student}")

else:
    st.success("✅ 모든 학생 출결 확인 완료")

# ---------------------------
# 출결 현황 조회
# ---------------------------
st.subheader("📋 출결 현황")

def highlight_status(row):
    color = {
        "출석": "#d4edda",
        "지각": "#fff3cd",
        "결석": "#f8d7da"
    }.get(row["상태"], "white")

    return [f"background-color: {color}"] * len(row)

styled_df = df.style.apply(highlight_status, axis=1)

st.dataframe(
    styled_df,
    use_container_width=True,
    hide_index=True
)

# ---------------------------
# CSV 다운로드
# ---------------------------
csv = df.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    "📥 출결 CSV 다운로드",
    csv,
    file_name="attendance.csv",
    mime="text/csv"
)

# ---------------------------
# 하단 안내
# ---------------------------
st.divider()

st.info(
    "아침 조례 시간에 학생 출결을 입력하고 "
    "결석 학생을 즉시 확인할 수 있습니다."
)
