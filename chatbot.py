import streamlit as st
import pandas as pd
import ollama
import matplotlib.pyplot as plt

# Title
st.title('소비TI 기반 ESG 금융 게임 플랫폼')

# Sidebar 메뉴
st.sidebar.header('메뉴')
option = st.sidebar.selectbox('선택하세요', ['미션 진행', '소비 분석', '랭킹', '친환경 미션', '소비 리포트'])

# 사용자 텍스트 기반 소비 데이터 입력
st.subheader('소비 패턴 분석')
user_input = st.text_area('최근 소비 내역을 자유롭게 작성해주세요. (예: 지난달에는 식비로 30만원, 교통비로 10만원을 사용했습니다.)')

# 시스템 프롬프트 불러오기
def load_system_prompt():
    return '''
**역할:**  
당신은 금융 데이터 분석 및 게임화 설계에 능숙한 AI 전문가입니다.  

**맥락:**  
우리는 금융 게임 플랫폼을 개발 중이며, 사용자 소비 패턴을 분석하고 개인화된 미션을 설계하여 절약과 친환경 소비를 유도하는 시스템을 구축하려고 합니다. 특히, ESG(환경, 사회, 지배구조) 요소를 반영해 사용자가 지속 가능한 소비 습관을 형성할 수 있도록 돕는 것이 목표입니다.  

**작업 지시:**  
- **소비 패턴 분석 및 미션 설계:**  
  사용자의 자유로운 텍스트 소비 내역을 분석해 소비 패턴을 파악하고, 절약 및 친환경 소비와 관련된 개인 맞춤형 미션을 설계하세요.  
  사용자가 제공하는 모든 소비 데이터를 활용하여 절약 가능성이 높은 부분을 식별하고, 친환경 소비 및 저축과 관련된 실행 가능한 미션을 3가지 제안하세요.  

**출력 형태:**  
- 사용자의 소비 패턴을 분석하고, 절약 및 친환경 소비를 유도하는 맞춤형 미션을 목록 형태로 작성하세요.
- 각 미션은 명확하고 측정 가능한 목표를 포함하세요.
- 미션 난이도를 3단계(쉬움, 보통, 어려움)로 구분하고, 예상 절약 금액을 명시하세요.
    '''

# Ollama 소비 패턴 분석 및 미션 생성
def analyze_spending(user_input):
    system_prompt = load_system_prompt()
    response = ollama.generate(
        model="benedict/linkbricks-llama3.1-korean:8b",
        prompt=f"{system_prompt}\n사용자 입력: {user_input}"
    )
    return response['response']

# 미션 진행
if option == '미션 진행':
    st.subheader('🌟 현재 미션')
    if user_input:
        mission = analyze_spending(user_input)
        st.write(f'AI 분석 미션: **{mission}**')
    else:
        st.write('소비 내역을 입력해주세요.')

    if st.button('미션 완료'):  
        st.success('🎉 미션 완료! 포인트 +50 적립')

# 소비 분석
elif option == '소비 분석':
    st.subheader('📊 소비 분석')
    if user_input:
        analysis = analyze_spending(user_input)
        st.write(analysis)
    else:
        st.write('소비 내역을 입력해주세요.')

# 랭킹 시스템
elif option == '랭킹':
    st.subheader('🏆 랭킹')
    ranking = {
        '사용자 A': 3200,
        '사용자 B': 2900,
        '사용자 C': 2700
    }
    st.write(pd.DataFrame(list(ranking.items()), columns=['사용자', '포인트']))

# 친환경 미션
elif option == '친환경 미션':
    st.subheader('🌱 친환경 미션 트래커')
    eco_missions = {
        '대중교통 이용': '10회 중 7회 완료',
        '일회용 컵 사용 줄이기': '15회 중 12회 완료',
        '장바구니 사용': '20회 중 15회 완료'
    }
    for mission, progress in eco_missions.items():
        st.write(f'**{mission}**: {progress}')
        st.progress(int(progress.split(' ')[0].replace('회', '')) / int(progress.split(' ')[2].replace('회', '')))

# 소비 리포트 시각화
elif option == '소비 리포트':
    st.subheader('📈 월간 소비 리포트')
    st.write('자유 텍스트 입력 기반으로 생성된 리포트입니다.')
    if user_input:
        analysis = analyze_spending(user_input)
        st.write(analysis)
    else:
        st.write('소비 내역을 입력해주세요.')

    if st.button('리포트 저장'):
        st.success('리포트가 PDF로 저장되었습니다!')
