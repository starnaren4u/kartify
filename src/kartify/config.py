import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
KARTIFY_ENV = os.getenv("KARTIFY_ENV", "development")
KARTIFY_LOG_LEVEL = os.getenv("KARTIFY_LOG_LEVEL", "INFO")
