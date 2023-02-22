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
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev zlib zlib-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
    --disabled-password \
    --no-create-home \
    django-user

# EXPLANATION OF RUN COMMAND ABOVE
# python -m venv /py
#   make virtual environment
# apk add
#   download postgress 
# rm -rf /tmp && \
#   removes tmp files that are no longer need
# adduser
#   adds user into the docker container because it's bad to use the root user

# update PATH env var, prepends /py/bin to existing PATH variable
ENV PATH="/py/bin:$PATH"

USER django-user
