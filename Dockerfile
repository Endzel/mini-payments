FROM python:3.7

RUN mkdir -p /opt/payments
WORKDIR /opt/payments

RUN apt-get update
RUN apt-get install zlib1g-dev -y

ADD requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

RUN apt-get install mysql-server -y

ADD ./ /opt/payments/

EXPOSE 8000
