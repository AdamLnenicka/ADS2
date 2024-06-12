# Use an official Python runtime as a parent image
FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY temperature_producer.py .

CMD ["python", "./temperature_producer.py"]
