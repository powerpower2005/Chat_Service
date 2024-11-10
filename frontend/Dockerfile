# 빌드 스테이지
FROM node:16 as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
RUN npm install --save-dev @babel/core @babel/eslint-parser
COPY . .
RUN npm run build

# 프로덕션 스테이지
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]