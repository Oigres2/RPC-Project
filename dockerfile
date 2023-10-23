FROM python:3.8

WORKDIR /usr/src/app

COPY . .

RUN pip install Pillow

CMD [ "python", "./server.py" ]
