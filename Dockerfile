FROM python:3.7-slim-stretch
MAINTAINER ntim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV USERNAME email
ENV PASSWORD changeme
ENV CLIENT_ID client_id
ENV CLIENT_SECRET client_secret
ENV DEVICE_ID device_id
CMD [ "python", "./app.py" ]
