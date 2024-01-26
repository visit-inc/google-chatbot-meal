# Python 이미지를 기반으로 설정
FROM python:3.8-slim

# 작업 디렉토리 설정
WORKDIR .

# 필요한 Python 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Python 스크립트 파일 복사
COPY main.py .

# 스크립트 실행
CMD ["python", "./main.py"]
