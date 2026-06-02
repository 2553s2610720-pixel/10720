import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="맛있는 음식 추천 챗봇", page_icon="🍔", layout="centered")
st.title("🍔 오늘 뭐 먹지? 맛있는 음식 고르기!")
st.write("결정 장애가 오셨나요? 무엇이 먹고 싶은지, 혹은 지금 기분이 어떤지 말씀해주시면 딱 맞는 음식을 추천해 드려요!")

# 2. Streamlit Secrets에서 API 키 불러오기 및 설정
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except KeyError:
    st.error("🚨 Streamlit Secrets에 'GOOGLE_API_KEY'가 설정되지 않았습니다. 대시보드 설정을 확인해주세요.")
    st.stop()

# 3. 세션 상태(Session State)를 이용한 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요! 오늘의 메뉴 선택을 도와드릴 푸드 가이드입니다. 탕수육 찍먹/부먹 같은 취향부터, 매콤한 게 당긴다거나 하는 현재 기분까지 편하게 말씀해주세요! 🍕✨"
        }
    ]

# 4. 기존 채팅 기록 화면에 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 5. 사용자 입력 받기
if user_input := st.chat_input("예: 매콤하고 면 종류인 음식 추천해줘!"):
    
    # 사용자 메시지 화면에 표시 및 기록 저장
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 6. Gemini API 호출 및 답변 생성 (오류 처리 포함)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # 모델 설정 (요청하신 gemini-2.5-flash-lite 사용)
            # 음식 추천에 집중할 수 있도록 시스템 지침(System Instruction) 부여
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash-lite",
                system_instruction="당신은 세상의 모든 맛있는 음식을 꿰고 있는 친절하고 유쾌한 음식 추천 전문가입니다. 사용자의 취향, 기분, 날씨 등에 맞춰 침이 고이는 맛있는 음식을 추천하고 그 이유를 설명해주세요."
            )
            
            # 대화 맥락 유지를 위해 기존 기록을 Gemini 형식으로 변환하여 전달
            # 단, Gemini API는 user/model 역할을 사용하므로 assistant를 model로 변환
            chat_history = []
            for msg in st.session_state.messages[:-1]: # 방금 넣은 user_input 제외한 이전 기록
                role = "model" if msg["role"] == "assistant" else "user"
                chat_history.append({"role": role, "parts": [msg["content"]]})
            
            # 대화 시작
            chat = model.start_chat(history=chat_history)
            
            # 스트리밍이 아닌 일반 답변 생성 (lite 모델의 빠른 응답 속도 활용)
            with st.spinner("음식 고르는 중... ⏳"):
                response = chat.send_message(user_input)
            
            # 답변 출력 및 저장
            ai_response = response.text
            message_placeholder.write(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            # API 키 오류, 네트워크 오류 등 예외 처리
            error_msg = f"죄송합니다. 답변을 생성하는 중에 오류가 발생했습니다. 😢 (오류 내용: {str(e)})"
            message_placeholder.error(error_msg)
