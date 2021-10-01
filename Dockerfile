###########
# BUILDER #
###########

# pull official base image
FROM python:3.9.6-alpine3.14 as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Needed for pycurl
ENV PYCURL_SSL_LIBRARY=openssl

# install psycopg2 dependencies
RUN apk update \
  && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev dcron \
  && rm -rf /var/cache/apk/*

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#########
# FINAL #
#########

# pull official base image
FROM python:3.9.6-alpine3.14

ENV PATH="/scripts:${PATH}"

# create directory for the app user
RUN mkdir -p /app

# create the appropriate directories
ENV APP_HOME=/app
WORKDIR $APP_HOME

# install dependencies
RUN apk update && apk add libpq
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy project
COPY ./manage.py $APP_HOME
COPY ./core $APP_HOME/core
COPY ./users $APP_HOME/users

COPY ./scripts /scripts

RUN chmod +x /scripts/*

# run entrypoint.sh
CMD ["entrypoint.sh"]