FROM python:3.9-alpine3.13
LABEL maintainer="fireflyteam"

# run python and dont buffer the outputs so they appear on the screen
ENV PYTHONUNBUFFERED 1

# copy local files into the docker container
COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app

# use /app as the dir to run commands in
WORKDIR /app

# define container port to access the container
EXPOSE 8000

# ARG DEV=false

# run a command when the alpine image is building
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev libpng && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev zlib zlib-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
    --disabled-password \
    --no-create-home \
    django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol


# EXPLANATION OF RUN COMMAND ABOVE
# python -m venv /py
#   make virtual environment
# apk add
#   download postgres client so that django can connect to the db
# apk add --virtual
#   groups deps into a virtual dep group ".tmp-build-deps" that contains build-base and following packages
# rm -rf /tmp && \
#   removes tmp files that are no longer need
# apk del .tmp-build-deps
#   removes the virtual dep group that was used only for installation of psycopg2
# adduser
#   adds user into the docker container because it's bad to use the root user

# update PATH env var, prepends /py/bin to existing PATH variable
ENV PATH="/py/bin:$PATH"

USER django-user
