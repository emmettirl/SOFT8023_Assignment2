FROM python:3.9-slim
WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt && apt-get update \
    && apt-get install -y iputils-ping

EXPOSE 12345

CMD ["python", "./server.py"]

