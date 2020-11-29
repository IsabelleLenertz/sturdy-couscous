FROM python:2
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY stale_checker.py ./
COPY ws_client.py ./

EXPOSE 8888

RUN pip install --no-cache-dir -r requirements.txt
