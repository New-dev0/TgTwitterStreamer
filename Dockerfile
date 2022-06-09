FROM python:latest

COPY . .

CMD ["python3", "-m", "TgTwitterStreamer"]