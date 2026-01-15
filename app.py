import streamlit as st
import google.generativeai as genai

# --- 1. 본인의 API 키를 입력하세요 ---
GOOGLE_API_KEY = "여기에_교수님의_키를_넣으세요" 

genai.configure(api_key=GOOGLE_API_KEY)
# 모델 이름을 가장 안정적인 'gemini-pro'로 변경했습니다.
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="정신간호 MSE 실습 (AI)", layout="centered")

# (이하 코드 동일...)
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if st.session_state.step == 1:
    st.title("🏥 AI 기반 정신간호 MSE 실습")
    st.session_state.user_name = st.text_input("학생 성함")
    st.session_state.topic = st.selectbox("실습 주제 선택", [
        "조현병 환자 사정 (사례: 35세 여성, 환청과 불안)",
        "조울증 환자 사정 (사례: 32세 남성, 조증 상태)",
        "자살 위험 환자 사정 (사례: 26세 여성, 자살 충동)"
    ])
    
    if st.button("실습 시작"):
        st.session_state.system_prompt = f"너는 정신과 환자야. 주제는 {st.session_state.topic}이야. 비언어적 표현을 [ ]에 포함해서 간호학생과 대화해줘."
        st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 2:
    st.header(f"💬 대상자 대화 ({st.session_state.topic})")
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    if prompt := st.chat_input("질문을 입력하세요"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # AI 응답 생성 부분
        response = model.generate_content(f"{st.session_state.system_prompt}\n학생: {prompt}")
        st.session_state.chat_history.append({"role": "assistant", "content": response.text})
        st.rerun()

    if st.button("대화 종료 및 보고서 작성"):
        st.session_state.step = 3
        st.rerun()

elif st.session_state.step == 3:
    st.header("📝 MSE 사정 보고서")
    mse_result = st.text_area("사정 결과 기록")
    if st.button("제출 완료"):
        st.write(f"학습자: {st.session_state.user_name}")
        st.write(f"내용: {mse_result}")
        st.balloons()
