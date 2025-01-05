FROM python@sha256:9b0d7419e2811710aacee87c40a2c94693e2b6810c3e7e466b8c7fc5bde4cd66 AS builder

WORKDIR /mnt

COPY ./requirements.txt ./

RUN apt-get update
RUN apt-get install -y build-essential
RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt 
RUN pip3 install --verbose llama-cpp-python
# RUN pip3 install --no-cache-dir -f https://download.pytorch.org/whl/cpu/torch_stable.html
RUN rm -rf ~/.cache/pip