FROM python:3.9-slim-bullseye
COPY ./service /service

RUN pip install --upgrade pip
RUN pip install -r /service/requirements.txt

EXPOSE 5000/tcp

CMD ["python3", "-u", "./service/image_sftp.py"]
