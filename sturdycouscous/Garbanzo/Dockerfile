FROM python
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY Checker.py ./
COPY CheckTester.py ./
COPY ws_server.py ./
COPY ws_client.py ./
COPY redis.py ./

RUN pip install --no-cache-dir -r requirements.txt

# FOR DEV
RUN apt-get update
RUN apt-get install -y vim

# Redis
RUN apt-get install -y redis

EXPOSE 6379/tcp
EXPOSE 6379/udp

CMD redis-server
