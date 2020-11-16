FROM python
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY Checker.py ./
COPY CheckTester.py ./

RUN pip install --no-cache-dir -r requirements.txt

CMD python CheckTester.py
