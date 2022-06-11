FROM ubuntu:focal
WORKDIR /KSK
EXPOSE 8000
COPY    ./requirements.txt  ./
RUN apt-get update && apt-get install -y software-properties-common gcc && \
    add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y python3.6 python3-distutils python3-pip python3-apt python3-venv
RUN pip3 install -r requirements.txt && \
    pip3 install gunicorn
COPY ./ ./
CMD ["gunicorn","--bind","0.0.0.0:8000","-w","3","run:app"]
