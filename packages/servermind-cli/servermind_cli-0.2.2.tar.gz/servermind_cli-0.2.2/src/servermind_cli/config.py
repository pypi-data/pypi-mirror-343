import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# OpenAI API 키
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# GPT 모델 설정
GPT_MODEL = os.getenv("GPT_MODEL", "gpt-4")

# 로그 파일 경로
LOG_FILE = os.getenv("LOG_FILE", "history.log")

# 언어 설정
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "ko")  # 기본값 한국어 