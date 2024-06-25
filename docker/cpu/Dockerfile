FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get -y install --no-install-recommends\
    software-properties-common\
    libgl1-mesa-dev \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    mesa-utils \
    libglew-dev \
    libosmesa6-dev \
    fontconfig \
    libfreetype6-dev \
    wget\
    libssl-dev\
    curl\
    git\
    x11-apps \
    swig \
    patchelf

# Python (version 3.10) for safety gymnasium
RUN add-apt-repository ppa:deadsnakes/ppa && \
  apt-get update && apt-get install -y \
  python3.10 \
  python3.10-dev \
  python3.10-venv \
  python3.10-distutils \
  python3.10-tk

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
RUN pip3 install --upgrade pip
RUN pip3 install -U pip distlib setuptools wheel

# utils
RUN apt-get update && apt-get install -y htop vim ffmpeg 
# RUN pip3 install jupyterlab ipywidgets && \
#     echo 'alias jup="jupyter lab --ip 0.0.0.0 --port 8888 --allow-root &"' >> /root/.bashrc

# clear cache
RUN rm -rf /var/lib/apt/lists/*

# install pyOpenGL
RUN pip3 install PyOpenGL PyOpenGL_accelerate

# pytorch for CPU only
RUN pip3 install torch==2.2.2 torchvision==0.17.2 --extra-index-url https://download.pytorch.org/whl/cpu

WORKDIR /workspace
COPY safepo/ safepo/
COPY setup.py .

RUN pip3 install -e .[dev]

CMD ["bash"]

