FROM python:3

ADD stock_db .

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]
