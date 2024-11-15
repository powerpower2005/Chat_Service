# 빌드 스테이지
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# serve 패키지 설치
RUN npm install -g serve

EXPOSE 3000

# serve로 dist 폴더 서빙
CMD ["serve", "-s", "dist", "-l", "3000"]