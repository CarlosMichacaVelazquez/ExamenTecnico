FROM python:3.9.5

WORKDIR /app

ENV FLASK_APP=main.py

ENV FLASK_RUN_HOST=0.0.0.0

ENV FLASK_DEBUG=1

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["flask","run"]