import streamlit as st
import google.generativeai as genai

# --- 1. 본인의 API 키 입력 (꼭 다시 넣으세요!) ---
GOOGLE_API_KEY = "여기에_교수님의_키를_넣으세요" 

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="정신간호 MSE 실습 (AI)", layout="centered")

# 세션 초기화
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'step' not in st.session_state:
    st.session_state.step = 1

# --- 1단계: 정보 입력 ---
if st.session_state.step == 1:
    st.title("🏥 AI 기반 정신간호 MSE 실습")
    name = st.text_input("학생 성함", key="user_name_input")
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
    
    # 이전 대화 내용 표시
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # 채팅 입력창
    if prompt := st.chat_input("대상자에게 질문을 던져보세요"):
        # 학생 질문 표시
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI 답변 생성 (로딩 아이콘 표시)
        with st.chat_message("assistant"):
            with st.spinner("대상자가 답변을 생각 중입니다..."):
                try:
                    full_prompt = f"너는 정신과 환자야. {st.session_state.topic} 상황에 맞춰서 대답해줘. 비언어적 표현을 [ ]에 포함해줘. 학생의 질문: {prompt}"
                    response = model.generate_content(full_prompt)
                    answer = response.text
                    st.markdown(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"AI 응답 중 오류가 발생했습니다: {e}")

    st.divider()
    if st.button("대화 종료 및 보고서 작성"):
        st.session_state.step = 3
        st.rerun()

# --- 3단계: 보고서 작성 ---
elif st.session_state.step == 3:
    st.header("📝 MSE 사정 보고서")
    mse_result = st.text_area("사정 결과 기록", height=200)
    if st.button("최종 제출"):
        st.success("실습이 완료되었습니다!")
        st.write(f"**학습자:** {st.session_state.user_name}")
        st.write(f"**작성한 MSE 사정:** {mse_result}")
        st.balloons()
