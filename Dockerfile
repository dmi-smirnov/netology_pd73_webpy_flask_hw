FROM python:3.10.12

WORKDIR /usr/src/app

COPY ./flask_project .

RUN pip install -r requirements.txt

CMD gunicorn app:app -b 0.0.0.0:80