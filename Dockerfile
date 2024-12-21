# Ubuntu 기반의 최신 이미지 사용
FROM ubuntu:latest

# 기본 패키지 업데이트 및 설치
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Ollama 설치
RUN curl -fsSL https://ollama.com/install.sh | bash

# 프로젝트 파일 복사
WORKDIR /app
COPY . /app

# Python 라이브러리 설치
RUN pip3 install -r requirements.txt

# Ollama 서버와 Streamlit 앱 동시 실행
CMD ollama serve & streamlit run chatbot.py
