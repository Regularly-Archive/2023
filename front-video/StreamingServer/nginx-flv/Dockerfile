FROM nginx:stable-alpine as deploy
ARG NGINX_VERSION=1.22.1
    

# 编译 Nginx 
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
RUN apk add --no-cache --virtual .build-deps git gcc libc-dev make openssl-dev pcre2-dev zlib-dev linux-headers libxslt-dev gd-dev geoip-dev perl-dev libedit-dev mercurial bash alpine-sdk findutils && \    
    cd /usr/src; \
    git clone https://github.com/winshining/nginx-http-flv-module.git /usr/src/nginx-http-flv-module/ && \
    wget http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz; \ 
    tar -zxvf nginx-${NGINX_VERSION}.tar.gz; \ 
    cd nginx-${NGINX_VERSION}; \
    CONFARGS=$(nginx -V 2>&1 | sed -n -e 's/^.*arguments: //p') \
    CONFARGS=${CONFARGS/-Os -fomit-frame-pointer -g/-Os} && \
    echo $CONFARGS && \
    ./configure --with-compat $CONFARGS --add-module=/usr/src/nginx-http-flv-module/ && \
    make && make install && \
    apk del .build-deps && \
    rm -rf /tmp/* && rm -rf /var/cache/apk/* && rm -rf /usr/src/ 


# 复制配置、证书文件
COPY index.html /usr/nginx/wwwroot/index.html
COPY /nginx/ssl/ /usr/nginx/ssl/
COPY /nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
EXPOSE 1935
EXPOSE 443
CMD ["nginx", "-g", "daemon off;"]

