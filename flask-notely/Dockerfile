FROM python:3.12-slim as builder

WORKDIR /app
# Environment variables to prevent bytecode generation and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends gcc

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels


FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

COPY ./application ./application
COPY __init__.py .
COPY config.py .
COPY setup_db.py .
COPY init_app.py .
COPY app.py .
EXPOSE 5001

CMD ["python", "app.py"]
#CMD ["bash", "-c", "tail -f /dev/null"]