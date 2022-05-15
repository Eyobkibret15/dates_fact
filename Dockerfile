FROM ubuntu:latest


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update

#libpq-dev contains a minimal set of `PostgreSQL`_ binaries and headers requried
#for building 3rd-party applications for `PostgreSQL

RUN apt-get -y install libpq-dev gcc
RUN apt-get upgrade -y

# python3-dev and unixodbc  to make setup for some packeges like podbc
RUN apt-get install -y python3 python3-dev unixodbc-dev
RUN apt-get install python3-pip -y
# Update the image to the latest packages

WORKDIR /app
COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

ADD . /app/
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]