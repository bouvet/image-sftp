FROM python:3-alpine
COPY ./service /service

RUN apk update
RUN apk add openssl-dev libffi-dev musl-dev gcc make
RUN apk add build-base jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib
RUN pip install --upgrade pip

RUN pip install -r /service/requirements.txt

EXPOSE 5000/tcp

CMD ["python3", "-u", "./service/image_sftp.py"]
