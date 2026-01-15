import streamlit as st
import random

# --- 설정 ---
st.set_page_config(page_title="정신간호 MSE 실습", layout="centered")

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# --- 1단계: 정보 입력 ---
if st.session_state.step == 1:
    st.title("🏥 정신간호 MSE 실습 시작")
    name = st.text_input("이름")
    topic = st.selectbox("실습 주제 선택", ["조현병 환자 사정", "조울증 환자 사정", "자살 위험 환자 사정"])
    if st.button("실습 시작"):
        st.session_state.user_name = name
        st.session_state.topic = topic
        st.session_state.step = 2
        st.rerun()

# --- 2단계: 대화창 (이 부분이 추가되었습니다) ---
elif st.session_state.step == 2:
    st.header(f"💬 대상자 대화 연습 ({st.session_state.topic})")
    st.info("대상자에게 질문을 던져보세요. (예: 요즘 기분이 어떠신가요?)")

    # 대화창 구현
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.write(chat["content"])

    if prompt := st.chat_input("질문을 입력하세요"):
        # 학생 메시지 표시
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # 환자의 반응 설정 (주제별 랜덤 반응 예시)
        responses = {
            "조현병 환자 사정": ["[불안한 눈빛으로 주변을 살피며] 저 소리 안 들려요? 자꾸 저보고 나가라고 하잖아요...", "[귀를 막으며] 아니에요, 전 아무 잘못 없어요."],
            "조울증 환자 사정": ["[매우 빠른 말투로] 제가 지금 할 일이 너무 많아요! 이건 국가적인 프로젝트라니까요?", "[의자에서 들썩이며] 선생님도 같이 하실래요? 지금 기분이 너무 최고거든요!"],
            "자살 위험 환자 사정": ["[고개를 숙이고 작은 목소리로] 그냥... 다 끝내고 싶어요. 아무 의미가 없거든요.", "[창밖을 멍하니 바라보며] 저한테 왜 물어보시는 거예요? 어차피 똑같을 텐데."]
        }
        
        re = random.choice(responses[st.session_state.topic])
        st.session_state.chat_history.append({"role": "assistant", "content": re})
        st.rerun()

    if st.button("대화 종료 및 MSE 작성"):
        st.session_state.step = 3
        st.rerun()

# --- 3단계: MSE 작성 ---
elif st.session_state.step == 3:
    st.header("📝 MSE 사정지 작성")
    mse = st.text_area("사정한 내용을 기록하세요.")
    if st.button("최종 제출"):
        st.success("과제가 성공적으로 기록되었습니다!")
        st.balloons()
