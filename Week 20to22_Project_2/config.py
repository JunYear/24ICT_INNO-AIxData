# config.py
import os
from dotenv import load_dotenv

# 현재 파일의 디렉토리를 기준으로 .env 파일의 경로 설정
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGO_URI = os.environ.get('MONGO_URI')
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 최대 업로드 파일 크기 설정 (100MB)
