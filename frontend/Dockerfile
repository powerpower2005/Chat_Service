# 빌드 스테이지
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# 프로덕션 스테이지
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

# NGINX 설정에서 AIO 비활성화 
RUN echo "worker_processes 1;" > /etc/nginx/nginx.conf \
    && echo "events { worker_connections 1024; use epoll; }" >> /etc/nginx/nginx.conf
 
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]