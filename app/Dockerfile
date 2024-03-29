# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev git

# this is for Pillow
RUN apk add -u libpq jpeg-dev zlib-dev libjpeg

# this is for coincurve
RUN apk add autoconf automake build-base libffi-dev libtool pkgconfig python3-dev

# install dependencies
RUN pip install --upgrade pip
RUN pip install wheel
COPY ./requirements.txt .
RUN pip install -U -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
