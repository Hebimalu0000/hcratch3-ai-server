FROM python:3.9-alpine

WORKDIR /app

COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

RUN rm -rf /root/.cache

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
