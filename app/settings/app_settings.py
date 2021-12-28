import json
import os
from pydantic import AnyHttpUrl, AnyUrl, BaseSettings, EmailStr, validator
from typing import List, Set, Union, get_type_hints
# Literal from typing_extensions for python 3.7 support, remove if not needed
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
#
from app.utils.helpers import SingleInstanceMetaClass, get_env_variable


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
        if settings_path:
            settings_json_path = os.path.join(Settings.current_dir, settings_path)
            settings_json = json.loads(open(settings_json_path, 'r').read())
        else:
            settings_json = dict()
        
        Settings.ALGORITHM = get_env_variable("ALGORITHM", settings_json, str)
        Settings.SECRET_KEY = get_env_variable("SECRET_KEY", settings_json, str)
        Settings.ENVIRONMENT = get_env_variable("ENVIRONMENT", settings_json, str)
        Settings.ACCESS_TOKEN_EXPIRE_MINUTES = get_env_variable("ACCESS_TOKEN_EXPIRE_MINUTES", settings_json, str)
        Settings.REFRESH_TOKEN_EXPIRE_MINUTES = get_env_variable("REFRESH_TOKEN_EXPIRE_MINUTES", settings_json, str)
        Settings.BACKEND_CORS_ORIGINS = get_env_variable("BACKEND_CORS_ORIGINS", settings_json, str)
    
    @classmethod
    def print(self):
        settings = \
        f"""
        Settings
        {"-"*50}
        ALGORITHM: {Settings.ALGORITHM}
        SECRET_KEY: {Settings.SECRET_KEY}
        ENVIRONMENT: {Settings.ENVIRONMENT}
        ACCESS_TOKEN_EXPIRE_MINUTES: {Settings.ACCESS_TOKEN_EXPIRE_MINUTES}
        REFRESH_TOKEN_EXPIRE_MINUTES: {Settings.REFRESH_TOKEN_EXPIRE_MINUTES}
        BACKEND_CORS_ORIGINS: {Settings.BACKEND_CORS_ORIGINS}
        {"-"*50}
        """
        return settings
    
    @classmethod
    def get_cors_list(self):
        try:
            return Settings.BACKEND_CORS_ORIGINS.split(",")
        except:
            return ["*"]


settings_path = 'settings.json'
Settings().load_settings(settings_path)
