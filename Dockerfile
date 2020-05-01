FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive
ARG DB_HOST
ARG DB_USER
ARG DB_PASSWORD
ARG STAGE
ARG JWT_SECRET

RUN echo ${STAGE}
RUN apt-get -y update && \
    apt-get install -y build-essential checkinstall wget \
    libreadline-gplv2-dev libncursesw5-dev libssl-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev \
    libapache2-mod-wsgi-py3 libpq-dev postgresql

RUN apt-get install -y python3.8 python3-pip curl r-base \
	build-essential \
    python3-dev \
    libmysqlclient-dev \
    build-essential \
    git \
    ssh \
    gunicorn3

RUN mkdir -p /opt/jukeboxradio
RUN chmod 777 /opt/jukeboxradio

COPY requirements.txt /opt/jukeboxradio/requirements.txt
COPY manage.py /opt/jukeboxradio/manage.py
COPY . /opt/jukeboxradio

WORKDIR /opt/jukeboxradio

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN export PYTHONPATH=`which python3`

EXPOSE 8000
RUN export PYTHONPATH=.
CMD ["daphne", "-p", "8000", "proj.asgi:application"]
