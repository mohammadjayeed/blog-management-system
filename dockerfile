FROM python:3.11-slim
ENV PYTHONBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN apt-get update -y
RUN apt-get install pkg-config -y
RUN apt-get install -y python3-dev build-essential
RUN apt-get install -y default-libmysqlclient-dev
COPY script.sh /script.sh
RUN chmod +x /script.sh
RUN pip install -r requirements.txt
COPY . .