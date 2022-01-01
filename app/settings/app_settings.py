import json
import os
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader
from jinja2.utils import select_autoescape
from pydantic import AnyHttpUrl, AnyUrl, validator
from typing import Any, Dict, List, Literal, Optional, Set, Union
#
from app.utils.helpers import SingleInstanceMetaClass, get_env_variable, pretty_text, remove_hidden_vars_fun_and_methods


class Config_Settings_Base():
    @classmethod
    def print(cls, boundary="=", boundary_length=100, separator="\n", indentation_text="\t"):
        class_name = cls.__name__
        dunder_dict = cls.__dict__
        class_variables = remove_hidden_vars_fun_and_methods(dunder_dict)
        key_value_dict = {class_variable: getattr(
            cls, class_variable) for class_variable in class_variables}
        text = pretty_text(class_name, key_value_dict, boundary,
                           boundary_length, separator, indentation_text)
        return text

    def load(self):
        raise NotImplementedError


class Settings(Config_Settings_Base, metaclass=SingleInstanceMetaClass):
    app_root_dir: str = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    current_dir: str = os.path.dirname(os.path.abspath(__file__))

    # These are class variables, and not instance variables as they are not initialized/set using self
    # https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables

    # https://stackoverflow.com/questions/20599375/what-is-the-purpose-of-checking-self-class
    # https://stackoverflow.com/questions/1060499/difference-between-typeobj-and-obj-class/10633356#10633356

    # CORE SETTINGS
    ALGORITHM: str = None
    SECRET_KEY: str = None
    ENVIRONMENT: Literal["DEV", "PYTEST", "STAGE", "PRODUCTION"] = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = None
    REFRESH_TOKEN_EXPIRE_MINUTES: int = None
    BACKEND_CORS_ORIGINS: Union[str, List[AnyHttpUrl]] = None

    def load(self, settings_path=None):
        if settings_path:
            settings_json_path = os.path.join(
                Settings.current_dir, settings_path)
            settings_json = json.loads(open(settings_json_path, 'r').read())
        else:
            settings_json = dict()

        Settings.ALGORITHM = get_env_variable("ALGORITHM", settings_json, str)
        Settings.SECRET_KEY = get_env_variable(
            "SECRET_KEY", settings_json, str)
        Settings.ENVIRONMENT = get_env_variable(
            "ENVIRONMENT", settings_json, str)
        Settings.ACCESS_TOKEN_EXPIRE_MINUTES = get_env_variable(
            "ACCESS_TOKEN_EXPIRE_MINUTES", settings_json, int)
        Settings.REFRESH_TOKEN_EXPIRE_MINUTES = get_env_variable(
            "REFRESH_TOKEN_EXPIRE_MINUTES", settings_json, int)
        Settings.BACKEND_CORS_ORIGINS = get_env_variable(
            "BACKEND_CORS_ORIGINS", settings_json, str)

    @classmethod
    def get_cors_list(self):
        if Settings.BACKEND_CORS_ORIGINS:
            return [item.strip() for item in Settings.BACKEND_CORS_ORIGINS.split(",")]
        else:
            return []


class EmailSettings(Config_Settings_Base, metaclass=SingleInstanceMetaClass):
    app_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    current_dir = os.path.dirname(os.path.abspath(__file__))

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None
    EMAIL_CREATE_ACCOUNT_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "templates"
    EMAILS_ENABLED: bool = False

    EMAIL_TEST_USER: str = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: str = None
    FIRST_SUPERUSER_PASSWORD: str = None
    USERS_OPEN_REGISTRATION: bool = False
    JINJA_ENVIRONMENT: Environment = None

    def load(self, email_settings_path=None):
        if email_settings_path:
            email_settings_json_path = os.path.join(
                Settings.current_dir, email_settings_path)
            email_settings_json = json.loads(
                open(email_settings_json_path, 'r').read())
        else:
            email_settings_json = dict()

        EmailSettings.SMTP_TLS = get_env_variable(
            "SMTP_TLS", email_settings_json, bool, EmailSettings.SMTP_TLS)
        EmailSettings.SMTP_PORT = get_env_variable(
            "SMTP_PORT", email_settings_json, int, EmailSettings.SMTP_PORT)
        EmailSettings.SMTP_HOST = get_env_variable(
            "SMTP_HOST", email_settings_json, str, EmailSettings.SMTP_HOST)
        EmailSettings.SMTP_USER = get_env_variable(
            "SMTP_USER", email_settings_json, str, EmailSettings.SMTP_USER)
        EmailSettings.SMTP_PASSWORD = get_env_variable(
            "SMTP_PASSWORD", email_settings_json, str, EmailSettings.SMTP_PASSWORD)
        EmailSettings.EMAILS_FROM_EMAIL = get_env_variable(
            "EMAILS_FROM_EMAIL", email_settings_json, str, EmailSettings.EMAILS_FROM_EMAIL)
        EmailSettings.EMAILS_FROM_NAME = get_env_variable(
            "EMAILS_FROM_NAME", email_settings_json, str, EmailSettings.EMAILS_FROM_NAME)
        EmailSettings.EMAIL_CREATE_ACCOUNT_TOKEN_EXPIRE_HOURS = get_env_variable(
            "EMAIL_CREATE_ACCOUNT_TOKEN_EXPIRE_HOURS", email_settings_json, int, EmailSettings.EMAIL_CREATE_ACCOUNT_TOKEN_EXPIRE_HOURS)
        EmailSettings.EMAIL_RESET_TOKEN_EXPIRE_HOURS = get_env_variable(
            "EMAIL_RESET_TOKEN_EXPIRE_HOURS", email_settings_json, int, EmailSettings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
        EmailSettings.EMAIL_TEMPLATES_DIR = get_env_variable(
            "EMAIL_TEMPLATES_DIR", email_settings_json, str, EmailSettings.EMAIL_TEMPLATES_DIR)
        EmailSettings.EMAILS_ENABLED = get_env_variable(
            "EMAILS_ENABLED", email_settings_json, bool, EmailSettings.EMAILS_ENABLED)
        EmailSettings.EMAIL_TEST_USER = get_env_variable(
            "EMAIL_TEST_USER", email_settings_json, str, EmailSettings.EMAIL_TEST_USER)
        EmailSettings.FIRST_SUPERUSER = get_env_variable(
            "FIRST_SUPERUSER", email_settings_json, str, EmailSettings.FIRST_SUPERUSER)
        EmailSettings.FIRST_SUPERUSER_PASSWORD = get_env_variable(
            "FIRST_SUPERUSER_PASSWORD", email_settings_json, str, EmailSettings.FIRST_SUPERUSER_PASSWORD)
        EmailSettings.USERS_OPEN_REGISTRATION = get_env_variable(
            "USERS_OPEN_REGISTRATION", email_settings_json, bool, EmailSettings.USERS_OPEN_REGISTRATION)
        EmailSettings.JINJA_ENVIRONMENT = Environment(loader=FileSystemLoader(os.path.join(EmailSettings.app_root_dir,
            EmailSettings.EMAIL_TEMPLATES_DIR)), autoescape=select_autoescape('xml', 'html'))

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )


settings_path = 'settings.json'
Settings().load(settings_path)

email_settings_path = 'email_settings.json'
EmailSettings().load(email_settings_path)
