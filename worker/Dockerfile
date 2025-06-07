FROM python:3.12-slim

WORKDIR /worker

COPY requirements.txt /worker/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./consumer.py /worker/

CMD ["python", "consumer.py"]
