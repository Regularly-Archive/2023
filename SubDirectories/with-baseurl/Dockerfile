# app1
FROM node:lts-alpine as app1_build
WORKDIR /app
COPY /app1/package*.json ./
RUN npm install -g cnpm --registry=https://registry.npm.taobao.org
RUN cnpm install
COPY /app1/ ./
RUN npm run build

# app12
FROM node:lts-alpine as app2_build
WORKDIR /app
COPY /app2/package*.json ./
RUN npm install -g cnpm --registry=https://registry.npm.taobao.org
RUN cnpm install
COPY /app2/ ./
RUN npm run build

# deploy
FROM nginx:stable-alpine as deploy
COPY --from=app1_build /app/dist/ /usr/nginx/wwwroot
COPY --from=app2_build /app/dist/ /usr/nginx/wwwroot/app2/
COPY /nginx/ssl/ /usr/nginx/ssl/
COPY /nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

