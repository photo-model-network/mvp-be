# Python 3.10.14 이미지를 사용
FROM python:3.10.14

# 빌드 시간에 사용할 환경 변수를 선언
ARG NEW_RELIC_API_KEY
ARG NEW_RELIC_ACCOUNT_ID

# 환경 변수를 ENV로 설정하여 모든 RUN, CMD, ENTRYPOINT에서 사용 가능하게 만듦
ENV NEW_RELIC_API_KEY=${NEW_RELIC_API_KEY}
ENV NEW_RELIC_ACCOUNT_ID=${NEW_RELIC_ACCOUNT_ID}

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# New Relic CLI 설치 및 설정
RUN curl -Ls https://download.newrelic.com/install/newrelic-cli/scripts/install.sh | bash \
    && /usr/local/bin/newrelic install -n logs-integration

# 애플리케이션 소스 복사
COPY . /app

# 포트 설정 (애플리케이션이 사용할 포트)
EXPOSE 8000

# 애플리케이션 실행 (예: Uvicorn을 사용하여 ASGI 앱 실행)
CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
