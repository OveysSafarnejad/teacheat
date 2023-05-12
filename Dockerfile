FROM python:3.10-alpine3.13


LABEL maintainer="safarnejad@outlook.com"
ENV PYTHONUNBUFFERD 1


COPY requirements.txt /app/requirements.txt
COPY ./.env /app/.env
COPY ./src /app/src
COPY ./scripts /app/scripts

WORKDIR /app/src

RUN python3 -m venv /app/.venv && \
    # packages for psycopg2 in alpine version of base image
    apk add --update --no-cache postgresql-client && \
    # unneccessary packages can be removed after installing requirements using --virtual .tmp-deps 
    apk add --update --no-cache --virtual .tmp-deps \
    build-base postgresql-dev musl-dev linux-headers && \
    #
    /app/.venv/bin/pip install --upgrade pip && \
    /app/.venv/bin/pip install -r /app/requirements.txt && \
    # removing unneccessary packages
    apk del .tmp-deps && \
    # creating non-root user for limitted permissions
    addgroup -S appgroup && \
    adduser -S appuser -G appgroup --disabled-password --no-create-home appuser && \  
    
    # creating static and media dirs and giving access for R/W to the appuser
    mkdir -p /app/vol/web/static && \
    mkdir -p /app/vol/web/media && \
    chown -R :appgroup /app/vol && \
    chown -R appuser:appuser /app/vol && \
    chmod -R 755 /app/vol && \
    chmod -R +x /app/scripts


# adding python environment from /.venv to the path
# now-on any python command will use /.venv python interpreter 
ENV PATH="/app/scripts:/app/.venv/bin:$PATH"
# switching root user to appuser 
# the appuser does not have full access
USER appuser

EXPOSE 8000

CMD ["run.sh"]

