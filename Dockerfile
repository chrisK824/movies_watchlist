FROM python:3.9

RUN mkdir -p /app
WORKDIR /app
COPY ./src/* .
COPY ./requirements.txt .

RUN python3 -m pip install -r requirements.txt

EXPOSE 9999

CMD [ "python3", "main.py" ]