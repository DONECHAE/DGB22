import streamlit as st
import pandas as pd
import ollama
import matplotlib.pyplot as plt
from datetime import datetime
import random
from fpdf import FPDF
from PIL import Image


# 타이틀 및 애니메이션 효과
st.title('🎮 게임으로 저축!')
st.write('### 재미있게 절약하고, 소비 습관을 바꿔보세요!')
st.markdown('---')

# 로컬 파일 경로 설정
local_image_path = r"C:\Users\DC\OneDrive - 계명대학교\DC\2024\2024_DGB\chatbot_project\unnamed.png"

# 이미지 읽기 및 표시
try:
    image = Image.open(local_image_path)
    st.sidebar.image(image,  use_container_width=True)
except Exception as e:
    st.sidebar.error("이미지를 불러오는 데 실패했습니다.")
    st.sidebar.write(str(e))

st.sidebar.header('📋 메뉴')
option = st.sidebar.radio('원하는 기능을 선택하세요', ['🏅 미션 진행', '📊 소비 분석', '🏆 랭킹', '📈 소비 리포트'])

# 실제 있을법한 한 명의 소비 데이터 생성
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
    df = pd.DataFrame(data)

    def calculate_score(amount):
        if amount <= 10000:
            return 15
        elif amount <= 20000:
            return 35
        elif amount <= 50000:
            return 65
        else:
            return 90

    df['소비 점수'] = df['금액'].apply(calculate_score)
    return df

# Ollama 소비 패턴 분석 및 미션 생성 (내부 처리)
def analyze_spending(data):
    system_prompt = ''' 
**🧑‍💻 역할:** 금융 데이터 분석가 & ESG 미션 설계 전문가  
**🌍 맥락:** 사용자의 금융 데이터를 분석하여 불필요한 지출을 식별하고, 절약 및 친환경 활동을 촉진하는 미션을 생성합니다.

**📋 작업 지시:**  
1. **데이터 분류 및 점수 부여:**  
   - 소비 내역을 **사치품, 환경 유해 소비, 편의, 구독 서비스, 저축** 등으로 분류합니다.
   - 각 범주별로 **소비 점수 (0-100점)**를 지출 금액, 빈도, 환경 영향 등을 고려하여 부여합니다.

2. **섹터 분류:**  
   - 소비 점수를 기준으로 **4개의 섹터**로 나눕니다:
     1. **절약이 반드시 필요한 부분:** 사치품, 환경 유해 소비
     2. **적당한 절약이 필요한 부분:** 편의, 구독 서비스
     3. **절약이 필요 없는 부분:** 저축 등 필수적이거나 긍정적인 소비
     4. **절약을 통해 더 사용할 수 있는 부분:** 생필품, 편의

3. **미션 생성:**  
   - 각 섹터별로 **미션**을 생성합니다.
   - 각 미션은 다음 요소를 포함해야 합니다:
     - **미션 이름:** 직관적이고 흥미로운 타이틀
     - **목표 및 실행 방법:** 구체적이고 실행 가능한 목표
     - **난이도:** 쉬움 / 보통 / 어려움
     - **예상 절약 금액:** 명확한 금액 제시
     - **보상 및 인센티브:** 포인트, 할인 쿠폰 등

**📄 미션 템플릿:**

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

**섹터 분류 기준:**

1. **절약이 반드시 필요한 부분:** 사치품, 환경 유해 소비
2. **적당한 절약이 필요한 부분:** 편의, 구독 서비스
3. **절약이 필요 없는 부분:** 저축 등 필수적이거나 긍정적인 소비
4. **절약을 통해 더 사용할 수 있는 부분:** 생필품, 편의

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

# 데이터 생성 및 분석
data = generate_realistic_data()
mission = analyze_spending(data)
total_score = data['소비 점수'].mean()

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

elif option == '📈 소비 리포트':
    st.subheader('📈 소비 리포트')
    st.write('### 카테고리별 소비 내역')
    report = data.groupby('카테고리')['금액'].sum().reset_index()
    st.dataframe(report)
    if st.button('📥 리포트 PDF 다운로드'):
        pdf = generate_pdf_report(report)
        pdf.output("소비_리포트.pdf")
        st.success('리포트 PDF가 저장되었습니다!')
