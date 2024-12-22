import streamlit as st
import pandas as pd
import ollama
import matplotlib.pyplot as plt
from datetime import datetime
import random
from fpdf import FPDF
from PIL import Image

# 한글 폰트 및 마이너스 기호 설정
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False

# CSS 스타일 적용
st.markdown(
    """
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background-color: #FFFFFF;
    }
    .title {
        text-align: center;
        color: #00C6A9;
    }
    .mission-box {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .highlight {
        color: #00C6A9;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #00C6A9;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #009f8a;
    }
    .sidebar .stRadio > label {
        color: #666666;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 타이틀 및 애니메이션 효과
st.markdown('<h1 class="title">🎮 게임으로 저축!</h1>', unsafe_allow_html=True)
st.write('### 재미있게 절약하고, 소비 습관을 바꿔보세요!')
st.markdown('---')

# 이미지 경로 및 표시
local_image_path = r"C:\Users\DC\OneDrive - 계명대학교\DC\2024\2024_DGB\chatbot_project\unnamed.png"
try:
    image = Image.open(local_image_path)
    st.sidebar.image(image, use_container_width=True)
except Exception as e:
    st.sidebar.error("이미지를 불러오는 데 실패했습니다.")
    st.sidebar.write(str(e))

st.sidebar.header('📋 메뉴')
option = st.sidebar.radio('원하는 기능을 선택하세요', ['🏅 미션 진행', '📊 소비 분석', '🏆 랭킹', '📈 소비 리포트'])

# 더미 데이터 생성
@st.cache_data
def generate_realistic_data():
    data = {
         '날짜': pd.date_range(start='2024-01-01', periods=30, freq='D').tolist(),
        '항목': [
            '커피', '택시', '배달', '편의점', '쇼핑', '구독 서비스', '커피', '택시', '영화', '외식',
            '주유', '식료품', '책 구매', '배달', '의료비',
            '커피', '헬스장', '편의점', '구독 서비스', '의류 구매', '택시', '영화', '여행', '편의점',
            '쇼핑', '기타', '택시', '구독 서비스', '커피', '식료품'
        ],
        '금액': [4500, 12000, 25000, 5800, 32000, 15000, 4000, 13000, 15000, 28000,
                50000, 120000, 27000, 22000, 80000,
                4300, 55000, 6700, 13500, 58000, 13000, 17000, 300000, 7500,
                48000, 12000, 11000, 14500, 4500, 90000
        ],
        '카테고리': [
            '편의 지출', '교통', '식사', '편의 지출', '쇼핑', '구독 서비스', '편의 지출', '교통', '문화', '외식',
            '주유', '생활 필수', '교육', '식사', '의료',
            '편의 지출', '건강', '편의 지출', '구독 서비스', '의류', '교통', '문화', '여행', '편의 지출',
            '쇼핑', '기타', '교통', '구독 서비스', '편의 지출', '생활 필수'
        ]
    }
    return pd.DataFrame(data)

# Ollama 소비 패턴 분석 및 미션 생성 (내부 처리)
def analyze_spending(data):
    system_prompt = ''' 
당신은 금융 데이터 분석가이자 ESG 미션 설계 전문가입니다.  
사용자의 소비 내역을 분석하여 다음 기준에 따라 미션을 생성하세요:  
- 데이터는 사치품, 환경 유해 소비, 편의, 구독 서비스, 저축 등으로 분류됩니다.  
- 각 소비 범주에 점수(0-100)를 부여하고, 이를 기반으로 4개의 섹터로 나눕니다:  
  1. 절약이 반드시 필요한 부분 (사치품, 환경 유해 소비)  
  2. 적당한 절약이 필요한 부분 (편의, 구독 서비스)  
  3. 절약이 필요 없는 부분 (저축 등)  
  4. 절약을 통해 더 사용할 수 있는 부분 (생필품, 편의)  
  
각 섹터별로 아래의 미션 템플릿을 사용해 4개의 미션을 작성하세요. 결과물은 미션만 포함하며, 다른 설명은 생략합니다.  

**미션 템플릿:**  
---  
#### **미션 이름: [미션 제목]**  
- **목표 및 실행 방법:**  
  [구체적인 목표와 실행 방법]  
- **🎯 난이도:** [쉬움 / 보통 / 어려움]  
- **💰 예상 절약 금액:** [금액]  
- **🏆 보상 및 인센티브:**  
  - 게임 내 포인트: [포인트 수]점  
  - 할인 쿠폰: [쿠폰 내용]  
  - 기타 보상: [기타 내용]  
---  

**결과 예시:**  
---  
#### **미션 이름: 한 달간 커피 줄이기 챌린지**  
- **목표 및 실행 방법:**  
  한 달 동안 카페 커피 대신 집에서 커피를 내려 마시세요. 하루 1잔 카페 커피를 줄이면 됩니다.  
- **🎯 난이도:** 쉬움  
- **💰 예상 절약 금액:** 50,000원  
- **🏆 보상 및 인센티브:**  
  - 게임 내 포인트: 500점  
  - 할인 쿠폰: 커피 머신 할인 10%  
---  

결과물은 위와 같은 형식으로 출력됩니다.
    '''
    try:
        response = ollama.generate(
            model="benedict/linkbricks-llama3.1-korean:8b",
            prompt=f"{system_prompt}\n소비 데이터 분석:\n{data.to_string()}"
        )
        return response.get('response', '미션 설계에 실패했습니다.')
    except Exception as e:
        return f'오류 발생: {str(e)}'

# PDF 리포트 생성 함수
def generate_pdf_report(report):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="소비 리포트", ln=True, align='C')
    pdf.ln(10)
    for index, row in report.iterrows():
        pdf.cell(200, 10, txt=f"{row['카테고리']}: {row['금액']}원", ln=True)
    return pdf

# 소비 데이터 불러오기 및 분석
data = generate_realistic_data()
mission = analyze_spending(data)
total_score = data['금액'].mean()

if option == '🏅 미션 진행':
    st.subheader('🌟 현재 미션')
    st.info('AI가 분석한 결과, 아래 미션을 추천합니다!')
    with st.expander("🎯 미션 보기"):
        st.write(mission)

    if st.button('✅ 미션 완료!'):
        st.balloons()
        st.success('🎉 미션 완료! 포인트 +50 적립')

elif option == '🏆 랭킹':
    st.subheader('🏆 소비 점수 랭킹')
    ranking = pd.DataFrame({
        '순위': [1, 2, 3, 4],
        '사용자': ['사용자 A', '사용자 B', '나', '사용자 C'],
        '포인트': [max(total_score + 150, 0), max(total_score + 50, 0), max(total_score, 0), max(total_score - 100, 0)]
    })
    st.table(ranking)
    st.write(f'🏅 나의 랭킹: 3위 | 포인트: {max(total_score, 0):.2f}')

# 소비 조언 생성 함수 (LLM 활용)
def generate_advice_with_llm(report):
    total_spent = report['금액'].sum()
    summary_response = ollama.generate(
        model="benedict/linkbricks-llama3.1-korean:8b",
        prompt=f"총 소비 금액은 {total_spent}원입니다. 전체적인 소비 패턴을 분석하고 절약을 위한 전반적인 조언을 제공해 주세요."
    )
    st.write("**📊 전반적인 소비 분석:**")
    st.write(summary_response.get('response', '조언을 생성하는 데 실패했습니다.'))
    
    advice = []
    for _, row in report.iterrows():
        response = ollama.generate(
            model="benedict/linkbricks-llama3.1-korean:8b",
            prompt=f"{row['카테고리']} 항목의 소비 금액은 {row['금액']}원입니다. 절약을 위한 조언을 제공해 주세요."
        )
        advice.append(response.get('response', '조언을 생성하는 데 실패했습니다.'))
    return advice

# 소비 데이터 불러오기 및 분석
data = generate_realistic_data()

if option == '📈 소비 리포트':
    st.subheader('📈 소비 리포트')
    st.write('### 카테고리별 소비 내역')
    report = data.groupby('카테고리')['금액'].sum().reset_index()
    st.dataframe(report)
    advice_list = generate_advice_with_llm(report)
    for i, advice in enumerate(advice_list):
        st.write(f"**{report['카테고리'][i]}:** {advice}")
    st.button('📥 리포트 PDF 다운로드')

if option == '📊 소비 분석':
    st.subheader('📊 소비 분석')
    st.write('카테고리별 소비 데이터 시각화')

    # 카테고리별 지출 합계
    category_sum = data.groupby('카테고리')['금액'].sum().reset_index()

    # 바 차트
    st.bar_chart(category_sum, x='카테고리', y='금액')

    # 파이 차트
    fig, ax = plt.subplots()
    ax.pie(category_sum['금액'], labels=category_sum['카테고리'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # 원형으로 유지
    st.pyplot(fig)

    # 라인 차트 (일별 지출 패턴)
    st.line_chart(data, x='날짜', y='금액')

    # 데이터 테이블
    st.dataframe(data)
