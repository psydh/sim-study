import streamlit as st
import google.generativeai as genai

# --- 1. 본인의 API 키 입력 (따옴표 안에 꼭 넣으세요) ---
GOOGLE_API_KEY = "여기에_교수님의_키를_넣으세요" 

# API 설정 및 모델 로드 (가장 정확한 경로 지정)
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    # 모델 이름을 'models/gemini-1.5-flash'로 전체 경로를 적어줍니다.
    model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
except Exception as e:
    st.error(f"설정 중 오류가 발생했습니다: {e}")

st.set_page_config(page_title="정신간호 MSE 실습 (AI)", layout="centered")

# 세션 상태 초기화
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'step' not in st.session_state:
    st.session_state.step = 1

# --- 1단계: 초기 설정 ---
if st.session_state.step == 1:
    st.title("🏥 AI 기반 정신간호 MSE 실습")
    name = st.text_input("학생 성함")
    topic = st.selectbox("실습 주제 선택", [
        "조현병 환자 사정 (사례: 35세 여성, 환청과 불안)",
        "조울증 환자 사정 (사례: 32세 남성, 조증 상태)",
        "자살 위험 환자 사정 (사례: 26세 여성, 자살 충동)"
    ])
    
    if st.button("실습 시작"):
        if name:
            st.session_state.user_name = name
            st.session_state.topic = topic
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("이름을 입력해주세요.")

# --- 2단계: 실시간 AI 대화창 ---
elif st.session_state.step == 2:
    st.header(f"💬 대상자 대화 ({st.session_state.topic})")
    st.info("대상자에게 질문하여 MSE 사정을 진행하세요. (행동, 사고, 지각 등 관찰)")
    
    # 대화 기록 출력
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # 사용자 입력
    if prompt := st.chat_input("질문을 입력하세요"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI 답변 생성
        with st.chat_message("assistant"):
            with st.spinner("대상자가 반응하고 있습니다..."):
                try:
                    # 환자 페르소나 설정
                    system_instruction = f"너는 {st.session_state.topic} 진단을 받은 정신과 환자야. 간호학생의 질문에 맞춰서 증상을 보여줘. 반드시 [ ] 안에 비언어적 행동 묘사를 포함해줘. 너무 길게 말하지 말고 환자처럼 짧고 끊어서 말해줘."
                    response = model.generate_content(f"{system_instruction}\n학생: {prompt}")
                    
                    if response.text:
                        st.markdown(response.text)
                        st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error("AI 연결에 잠시 문제가 생겼습니다. 잠시 후 다시 시도하거나 키를 확인해주세요.")
                    st.info(f"상세 에러: {e}")

    if st.button("대화 종료 및 보고서 작성"):
        st.session_state.step = 3
        st.rerun()

# --- 3단계: 결과 확인 ---
elif st.session_state.step == 3:
    st.header("📝 MSE 사정 보고서")
    mse_result = st.text_area("사정 내용 기록 (행동, 기분, 사고과정 등)", height=250)
    if st.button("최종 제출"):
        st.success("실습 보고서가 작성되었습니다!")
        st.balloons()
        st.write(f"**학습자:** {st.session_state.user_name}")
        st.write(f"**사정 주제:** {st.session_state.topic}")
        st.write(f"**작성 내용:** {mse_result}")
