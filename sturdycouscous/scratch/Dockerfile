FROM python:2
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY test.py ./
COPY ws_client.py ./

EXPOSE 8888

RUN pip install --no-cache-dir -r requirements.txt
