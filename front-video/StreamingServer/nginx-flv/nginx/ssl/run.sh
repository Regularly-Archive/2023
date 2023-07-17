mkdir ./demoCA
mkdir demoCA/newcerts
vi demoCA/index.txt
vi demoCA/serial

#根证书
openssl genrsa -out ca.key 2048
openssl req -new -key ca.key -out ca.csr -subj "/C=CN/ST=SX/L=XA/O=snowfly/OU=snowfly/CN=*.snowfly.com"
openssl x509 -req -days 10000 -sha1 -extensions v3_ca -signkey ca.key -in ca.csr -out ca.cer

#服务器端证书
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr -subj "/C=CN/ST=SX/L=XA/O=snowfly/OU=snowfly/CN=*.snowfly.com"
openssl x509 -req -days 3650 -sha1 -extensions v3_req  -CA  ca.cer -CAkey ca.key  -CAcreateserial -in server.csr -out server.pem

# 客户端证书
openssl genrsa -des3 -out client.key 2048
openssl req -new -key client.key -out client.csr -subj "/C=CN/ST=SX/L=XA/O=snowfly/OU=snowfly/CN=*.snowfly.com"
openssl ca -days 3650 -in client.csr  -out client.cer -cert ca.cer -keyfile ca.key

