FROM python:3.8

WORKDIR /usr/src/app

COPY . .

RUN pip install Pillow
RUN pip install Requests
CMD [ "python", "./server.py" ]
