FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential iputils-ping
COPY agents /app
WORKDIR /app
RUN python3 -m pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["agents.py"]