import streamlit as st
import datetime

# --- 페이지 설정 ---
st.set_page_config(page_title="정신간호 MSE 시뮬레이션", layout="centered")

# --- 앱 스타일링 ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .scenario-box { background-color: #e9ecef; padding: 20px; border-radius: 10px; border-left: 5px solid #0d6efd; }
    .report-area { background-color: white; padding: 20px; border: 1px solid #dee2e6; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 세션 상태 관리 ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'student_info' not in st.session_state:
    st.session_state.student_info = {}

# --- 메인 로직 ---
st.title("🏥 정신간호 MSE 실습 시스템")

# [STEP 1: 정보 입력 및 주제 선택]
if st.session_state.step == 1:
    st.header("1단계: 학습자 정보 및 주제 선택")
    with st.container():
        name = st.text_input("성함")
        student_id = st.text_input("학번")
        
        st.subheader("실습 주제를 선택하세요")
        topic = st.radio(
            "오늘 수행할 MSE 주제:",
            ["주제1. 조현병 환자의 정신 상태 사정", 
             "주제2. 조울증 환자의 기분 상태 평가", 
             "주제3. 자살 위험이 높은 환자의 긴급 평가"]
        )
        
        if st.button("시나리오 확인 및 시작"):
            if name and student_id:
                st.session_state.student_info = {"name": name, "id": student_id, "topic": topic}
                st.session_state.step = 2
                st.rerun()
            else:
                st.error("이름과 학번을 입력해주세요.")

# [STEP 2: 시나리오 제시 및 역할극 지침]
elif st.session_state.step == 2:
    st.header("2단계: 시나리오 및 프롬프트 수행")
    
    topic = st.session_state.student_info['topic']
    
    st.markdown('<div class="scenario-box">', unsafe_allow_html=True)
    if "주제1" in topic:
        st.write("**[사례1]** 35세 여성 환자, 조현병 진단. 최근 환청이 심해져 불안해함.")
    elif "주제2" in topic:
        st.write("**[사례6]** 32세 남성 환자, 조울증 입원 중. 현재 조증 상태로 사고 비약이 보임.")
    else:
        st.write("**[사례]** 26세 여성 환자, 자살 충동 호소하며 응급실 방문.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.info("💡 **수행 지침:** 아래 프롬프트를 복사하여 ChatGPT나 수업용 AI에게 입력하고 10분간 대화를 진행하세요.")
    
    prompt_text = f"""진행계획을 알려줄게. 지금부터 너(ai)는 정신과 대상자의 역할을 하고, 나(사용자)는 정신과 간호학생으로 역할을 할 예정이야.
* 학습목표: 정신과 병동 대상자에 대한 간호중재를 적절하게 제공한다.
아래의 주제에 맞춰서 내가 간호학생으로 의사소통 연습을 할 수 있도록 10분간 환자 역할을 해줘. 장면과 비언어적 묘사도 포함해줘.
주제: {topic}"""
    
    st.code(prompt_text, language="text")
    
    if st.button("대화 완료 (3단계로 이동)"):
        st.session_state.step = 3
        st.rerun()

# [STEP 3: MSE 사정 작성]
elif st.session_state.step == 3:
    st.header("3단계: MSE 사정 기록지 작성")
    st.write("대화 내용을 바탕으로 전문 용어를 사용하여 사정 내용을 기록하세요.")
    
    mse_result = st.text_area("MSE 사정 내용 (외모, 사고, 기분, 지각 등)", height=300)
    comm_eval = st.text_area("치료적 의사소통 자가평가", placeholder="내가 사용한 치료적 의사소통 기법을 서술하세요.")
    
    if st.button("최종 리포트 생성"):
        st.session_state.mse_result = mse_result
        st.session_state.comm_eval = comm_eval
        st.session_state.step = 4
        st.rerun()

# [STEP 4: 최종 리포트 및 제출]
elif st.session_state.step == 4:
    st.header("✅ 과제 수행 완료")
    
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    
    report_html = f"""
    <div class="report-area">
        <h4>[사전학습 완료 보고서]</h4>
        <p><b>일시:</b> {now}</p>
        <p><b>학습자:</b> {st.session_state.student_info['name']} ({st.session_state.student_info['id']})</p>
        <p><b>선택주제:</b> {st.session_state.student_info['topic']}</p>
        <hr>
        <h5>1. MSE 사정 내용</h5>
        <p>{st.session_state.mse_result}</p>
        <h5>2. 치료적 의사소통 평가</h5>
        <p>{st.session_state.comm_eval}</p>
    </div>
    """
    st.markdown(report_html, unsafe_allow_html=True)
    
    st.warning("위 내용을 복사하여 과제 제출함에 붙여넣거나, 화면을 캡처하여 제출하세요.")
    
    if st.button("처음으로 돌아가기"):
        st.session_state.step = 1
        st.rerun()