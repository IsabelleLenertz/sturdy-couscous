FROM python
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY test_script.py ./

RUN pip install --no-cache-dir -r requirements.txt

CMD python test_script.py
