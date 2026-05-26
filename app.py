import random
import streamlit as st  # 오타 수정 완료!

# 1. 에러 방지용 기본 음식 데이터 정의
FOOD_DATA = {
    "한식": {
        "매운맛": ["떡볶이", "닭발", "김치찌개", "매운 갈비찜"],
        "담백/깔끔": ["비빔밥", "설렁탕", "삼계탕", "샤브샤브"],
        "달콤/짭조름": ["불고기", "갈비찜", "간장게장", "뚝배기 불고기"],
    },
    "일식": {
        "매운맛": ["탄탄멘", "매운 돈코츠 라멘", "카레 (매운맛)"],
        "담백/깔끔": ["초밥", "우동", "소바", "돈카츠"],
        "달콤/짭조름": ["규동", "가츠동", "장어덮밥", "야키토리"],
    },
    "중식": {
        "매운맛": ["마라탕", "마라샹궈", "짬뽕", "사천탕수육"],
        "담백/깔끔": ["울면", "백짬뽕", "딤섬"],
        "달콤/짭조름": ["짜장면", "탕수육", "꿔바로우", "동파육"],
    },
    "양식/기타": {
        "매운맛": ["아라비아따 파스타", "페페로니 피자", "타코"],
        "담백/깔끔": ["알리오 올리오", "리코타 치즈 샐러드", "샌드위치"],
        "달콤/짭조름": ["고르곤졸라 피자", "바베큐 폭립", "스테이크"],
    },
}

# 2. 웹앱 UI 설정
st.set_page_config(page_title="취향 저격 음식 추천", page_icon="🍔", layout="centered")

st.title("🍳 오늘 뭐 먹지? 취향 저격 추천!")
st.subheader("당신의 오늘 기분과 취향에 딱 맞는 음식을 추천해 드립니다.")
st.write("---")

# 3. 사이드바 사용자 입력 받기
st.sidebar.header("🎯 당신의 취향을 골라보세요")

# 음식 종류 선택
cuisine_options = list(FOOD_DATA.keys())
selected_cuisine = st.sidebar.selectbox("1. 어떤 종류의 음식을 원하시나요?", cuisine_options)

# 맛 선택
flavor_options = list(FOOD_DATA[selected_cuisine].keys())
selected_flavor = st.sidebar.selectbox("2. 지금 당기는 맛은?", flavor_options)

# 4. 추천 결과 출력 공간
st.markdown(f"### 📍 현재 선택: **{selected_cuisine}** > **{selected_flavor}**")

# 추천 버튼 클릭 이벤트
if st.button("🔥 음식 추천받기", use_container_width=True):
    # 안전하게 데이터 가져오기
    food_list = FOOD_DATA[selected_cuisine][selected_flavor]
    recommended_food = random.choice(food_list)

    # 화면에 효과와 함께 출력
    st.balloons()  # 폭죽 효과
    st.success(f"🎉 오늘 추천하는 메뉴는 바로 **[{recommended_food}]** 입니다!")
    st.info(f"💡 {selected_cuisine} 중에서 {selected_flavor}한 음식을 찾는 당신에게 딱 맞을 거예요!")
else:
    st.write("왼쪽 사이드바에서 취향을 고른 후, 위의 **[음식 추천받기]** 버튼을 눌러보세요!")
