FROM python:3.9

# 시스템 패키지 업데이트 및 필요한 도구 설치
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Node.js 설치 (Vue.js 개발용)
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs

# 작업 디렉토리 설정
WORKDIR /workspace

# Python 패키지 설치를 위한 requirements.txt 복사 및 설치
COPY /backend/requirements.txt /workspace/
RUN pip install -r /workspace/requirements.txt

# Vue CLI 설치
RUN npm install -g @vue/cli

# 기본 쉘을 bash로 설정
ENV SHELL /bin/bash