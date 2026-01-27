# loads environmental variables and app-wide settings
import os
from dotenv import load_dotenv

# Load the env
load_dotenv()

class Settings:
    PROJECT_NAME = 'Car Price Prediction API'
    API_KEY = os.getenv('API_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ALGORITHM = 'HS256'
    REDIS_URL = os.getenv('REDIS_URL')
    MODEL_PATH = 'app/models/model.joblib'
    ENV = os.getenv('ENV', 'development')

    def validate(self):
        if not self.API_KEY:
            raise RuntimeError("API_KEY is not set")
        if not self.JWT_SECRET_KEY:
            raise RuntimeError("JWT_SECRET_KEY is not set")

settings = Settings()
settings.validate()