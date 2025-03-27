import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


class Settings:

    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Single instance of the settings
settings = Settings()