FROM python
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY obtain_tls_version.py ./

RUN pip install --no-cache-dir -r requirements.txt

CMD python obtain-tls-version.py
