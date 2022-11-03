FROM python:latest

# RUN apt-get update -y && \  
#    apt-get install -y python3-pip python3-dev
WORKDIR /root/web_server/k8s_test
COPY . /root/web_server/k8s_test

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn gevent

CMD ["gunicorn", "app:app", "-c", "./gunicorn/config.py"]

# docker build -t web_server:v1 .