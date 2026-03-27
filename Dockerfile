FROM nginx:alpine

# 将本地所有文件（包括 index.html, data.json 等）拷贝到 Nginx 默认静态目录
COPY . /usr/share/nginx/html

# 暴露 80 端口（Nginx 默认）
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
