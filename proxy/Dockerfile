FROM nginxinc/nginx-unprivileged:1-alpine

LABEL maintainer='safarnejad@outlook.com'

COPY . /etc/nginx
COPY ./run.sh /run.sh

USER root

RUN mkdir -p /home/app/static && \
    chmod -R 755 /home/app/static && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh


# optional : useful when we want to deploy app on other service
VOLUME /home/app/static


USER nginx

CMD ["/run.sh"]