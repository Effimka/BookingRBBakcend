from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

#JWT vars
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM_JWT = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in environment")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY not set in environment")

