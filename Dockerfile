FROM python:3.9-slim-buster

RUN mkdir /imdb

WORKDIR /imdb

COPY ./ /imdb/

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]