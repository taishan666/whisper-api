FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime


COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY main.py whisper_script.py  Dockerfile .

ENTRYPOINT python3 main.py
