# app settings (env vars,CORS origins,etc)

from pydantic_settings import BaseSettings
from pydantic import ConfigDict

# BaseSettings read values from environment variables and .env files automatically.
# ConfigDict lets us configure how settings class bahaves.

class Settings(BaseSettings):
    model_config=ConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False # app_name and APP_NAME both work
    )
    APP_NAME:str='MathExpressionAPI'
    DEBUG:bool=False
    MODEL_PATH:str = "models/hmer.pt"
    API_V1_STR:str='/api/v1'
    FRONTEND_ORIGIN:str = "http://localhost:3000"


    
settings=Settings()
# create a Settings class that holds all your configuration values like app name, debug mode, model path, etc. Instead of hardcoding these values, pydantic automatically reads them from environment variables or a .env file — so you can change settings without touching your code.