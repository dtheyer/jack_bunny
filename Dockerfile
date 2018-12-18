FROM python:3.7.1-alpine3.8

RUN apk update && apk --no-cache add nginx

COPY code ./
RUN pip install --no-cache-dir -r /jack_bunny/requirements.txt

WORKDIR /jack_bunny

EXPOSE 80

COPY jack_bunny.nginx /etc/nginx/conf.d/default.conf
ENTRYPOINT gunicorn jack_bunny:app -p /var/run/jack_bunny.pid -D && nginx -c /etc/nginx/nginx.conf -g "pid /var/run/nginx.pid; daemon off;"
