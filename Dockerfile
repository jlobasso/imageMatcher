FROM ubuntu:18.04
FROM python:3.6.7

RUN apt-get update && \
        apt-get install -y \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        yasm \
        pkg-config \
        libswscale-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libavformat-dev \
        libpq-dev

RUN pip install opencv-python==3.3.0.10 opencv-contrib-python==3.3.0.10
RUN pip install numpy flask flask_restful flask_cors matplotlib

WORKDIR /

ADD . /

# EXPOSE 5002
# EXPOSE 8080
# CMD ["python", "serverFrontend.py"]
CMD ["python", "serverBakend.py"]
