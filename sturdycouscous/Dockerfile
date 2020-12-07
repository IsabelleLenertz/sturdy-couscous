FROM python
WORKDIR /usr/src/app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

#RUN mkdir -p history
#COPY history/ /history


RUN mkdir sturdycouscous
COPY . sturdycouscous/ 

CMD ["python", "sturdycouscous/SecurityCrawler.py"]

#CMD python Mongo_Client.py
