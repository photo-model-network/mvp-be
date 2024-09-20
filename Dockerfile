FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

WORKDIR /app

COPY requirements.txt .
COPY entrypoint.sh /app/entrypoint.sh

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000