# src/config.py

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    VECTORSTORE_PATH = "vectorstore"
    UPLOAD_FOLDER = "uploads"

settings = Settings()

# Validate required environment variables
if not settings.OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY is not set. Please add it to your .env file."
    )
