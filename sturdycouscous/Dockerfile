FROM python
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY Checker.py ./
COPY Mongo_Client.py ./

RUN pip install --no-cache-dir -r requirements.txt

CMD python Mongo_Client.py
