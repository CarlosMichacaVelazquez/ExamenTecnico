FROM python:3.9.5

WORKDIR /app

ENV FLASK_APP=main.py

ENV FLASK_DEBUG=1

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .

CMD ["flask","run"]