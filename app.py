import streamlit as st
import google.generativeai as genai

# --- 1. 여기에 키를 붙여넣으세요 ---
GOOGLE_API_KEY = "AIzaSyBVLA4WTbPf-o_gPpwCUeAwuPq5b94XS5I" 

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')

st.set_page_config(page_title="정신간호 MSE 실습 (AI)", layout="centered")

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# --- 2. 초기 설정 ---
if st.session_state.step == 1:
    st.title("🏥 AI 기반 정신간호 MSE 실습")
    st.session_state.user_name = st.text_input("학생 성함")
    st.session_state.topic = st.selectbox("실습 주제 선택", [
        "조현병 환자 사정 (사례: 35세 여성, 환청과 불안)",
        "조울증 환자 사정 (사례: 32세 남성, 조증 상태)",
        "자살 위험 환자 사정 (사례: 26세 여성, 자살 충동)"
    ])
    
    if st.button("실습 시작"):
        st.session_state.system_prompt = f"""
        너는 정신과 환자 역할을 하는 시뮬레이터야. 아래 설정에 맞춰서 간호학생과 대화해줘.
        주제: {st.session_state.topic}
        지침: 
        1. 대화할 때마다 너의 표정, 태도, 몸짓 등 비언어적 묘사를 [ ] 안에 반드시 포함해.
        2. 간호학생이 MSE 사정을 할 수 있도록 증상을 적절히 보여줘.
        3. 너무 협조적이지 않게, 실제 환자의 특성을 살려 대답해.
        4. 한국어로 대답해.
        """
        st.session_state.step = 2
        st.rerun()

# --- 3. 실시간 AI 대화창 ---
elif st.session_state.step == 2:
    st.header(f"💬 대상자 대화 ({st.session_state.topic})")
    
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    if prompt := st.chat_input("질문을 입력하세요"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI 답변 생성
        full_prompt = f"{st.session_state.system_prompt}\n\n학생 질문: {prompt}"
        response = model.generate_content(full_prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.chat_history.append({"role": "assistant", "content": response.text})

    if st.button("대화 종료 및 보고서 작성"):
        st.session_state.step = 3
        st.rerun()

# --- 4. 보고서 단계 ---
elif st.session_state.step == 3:
    st.header("📝 MSE 사정 보고서")
    mse_result = st.text_area("사정 결과 기록", height=200)
    if st.button("제출 완료"):
        st.success("실습이 완료되었습니다. 내용을 캡처하여 제출하세요.")
        st.write(f"학생: {st.session_state.user_name}")
        st.write(f"작성 내용: {mse_result}")
        st.balloons()

