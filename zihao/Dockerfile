FROM pytorch/pytorch:1.13.0-cuda11.6-cudnn8-runtime

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
