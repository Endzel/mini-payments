FROM python:3.13-slim-trixie

WORKDIR /opt/payments

COPY requirements.txt /tmp/
# mysqlclient has no prebuilt Linux wheels: compile it against the MariaDB client headers, then drop the toolchain
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential default-libmysqlclient-dev pkg-config && \
    pip install --no-cache-dir -r /tmp/requirements.txt && \
    apt-mark manual libmariadb3 && \
    apt-get purge -y --auto-remove build-essential default-libmysqlclient-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

COPY . /opt/payments/

EXPOSE 8000
