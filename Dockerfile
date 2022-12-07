FROM python:3.9

RUN mkdir -p /app
COPY src  /app
WORKDIR /app
RUN python3 -m pip install -r requirements.txt
EXPOSE 9999

CMD [ "python3", "main.py" ]