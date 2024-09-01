# Python 3.10.14 이미지를 사용
FROM python:3.10.14

# 작업 디렉토리 설정
WORKDIR /app

# sudo 설치
RUN apt-get update && apt-get install -y sudo

# 필요한 패키지 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# New Relic CLI 설치 및 설정 (sudo 사용)
RUN curl -Ls https://download.newrelic.com/install/newrelic-cli/scripts/install.sh | bash \
    && sudo NEW_RELIC_API_KEY=${NEW_RELIC_API_KEY} \
    && sudo NEW_RELIC_ACCOUNT_ID=${NEW_RELIC_ACCOUNT_ID} \
    && sudo /usr/local/bin/newrelic install -n logs-integration

# 애플리케이션 소스 복사
COPY . /app

# 포트 설정 (애플리케이션이 사용할 포트)
EXPOSE 8000

# 애플리케이션 실행 (예: Uvicorn을 사용하여 ASGI 앱 실행)
CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
