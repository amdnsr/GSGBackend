import json
import os
from pydantic import AnyHttpUrl, AnyUrl, BaseSettings, EmailStr, validator
from typing import List, Set, Union
# Literal from typing_extensions for python 3.7 support, remove if not needed
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
#
from app.utils.helpers import SingleInstanceMetaClass


class Settings(metaclass=SingleInstanceMetaClass):
    app_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # CORE SETTINGS
    ALGORITHM: str
    SECRET_KEY: str
    ENVIRONMENT: Literal["DEV", "PYTEST", "STAGE", "PRODUCTION"]
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    BACKEND_CORS_ORIGINS: Union[str, List[AnyHttpUrl]]

    def load_settings(self, settings_path=None):
        if not settings_path:
            Settings.ALGORITHM = os.getenv("ALGORITHM", None)
            Settings.SECRET_KEY = os.getenv("SECRET_KEY", None)
            Settings.ENVIRONMENT = os.getenv("ENVIRONMENT")
            Settings.ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", None)
            Settings.REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", None)
            Settings.BACKEND_CORS_ORIGINS = os.getenv("BACKEND_CORS_ORIGINS", None)
            return
        
        settings_json_path = os.path.join(Settings.current_dir, settings_path)
        settings_json = json.loads(open(settings_json_path, 'r').read())

        if settings_json["ALGORITHM"] is None:
            Settings.ALGORITHM = os.getenv("ALGORITHM", None)
        else:
            Settings.ALGORITHM = settings_json["ALGORITHM"]

        if settings_json["SECRET_KEY"] is None:
            Settings.SECRET_KEY = os.getenv("SECRET_KEY", None)
        else:
            Settings.SECRET_KEY = settings_json["SECRET_KEY"]

        if settings_json["ENVIRONMENT"] is None:
            Settings.ENVIRONMENT = os.getenv("ENVIRONMENT")
        else:
            Settings.ENVIRONMENT = settings_json["ENVIRONMENT"]

        if settings_json["ACCESS_TOKEN_EXPIRE_MINUTES"] is None:
            Settings.ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", None)
        else:
            Settings.ACCESS_TOKEN_EXPIRE_MINUTES = settings_json["ACCESS_TOKEN_EXPIRE_MINUTES"]

        if settings_json["REFRESH_TOKEN_EXPIRE_MINUTES"] is None:
            Settings.REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", None)
        else:
            Settings.REFRESH_TOKEN_EXPIRE_MINUTES = settings_json["REFRESH_TOKEN_EXPIRE_MINUTES"]

        if settings_json["BACKEND_CORS_ORIGINS"] is None:
            Settings.BACKEND_CORS_ORIGINS = os.getenv("BACKEND_CORS_ORIGINS", None)
        else:
            Settings.BACKEND_CORS_ORIGINS = settings_json["BACKEND_CORS_ORIGINS"]
    
    @classmethod
    def get_cors_list(self):
        try:
            return Settings.BACKEND_CORS_ORIGINS.split(",")
        except:
            return ["*"]


settings_path = 'settings.json'
Settings().load_settings(settings_path)
