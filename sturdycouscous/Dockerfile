FROM python
WORKDIR /usr/src/app
COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD python Mongo_Client.py
