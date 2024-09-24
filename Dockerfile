FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

WORKDIR /app

COPY requirements.txt entrypoint.sh ./

RUN pip install \
    --no-cache-dir \
    --upgrade \
    -r requirements.txt

COPY . .

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000