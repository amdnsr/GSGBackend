import json
import os
from typing import List
from app.settings.app_settings import Config_Settings_Base
from app.utils.helpers import SingleInstanceMetaClass, get_env_variable


class DBConfig(Config_Settings_Base, metaclass=SingleInstanceMetaClass):
    app_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    current_dir = os.path.dirname(os.path.abspath(__file__))

    bus_journey_details: dict = None
    bus_details: dict = None
    agency_details: dict = None
    agency_user_details: dict = None
    journey_seat_details: dict = None
    user_info_details: dict = None
    user_ticket_details: dict = None
    ticket_payment_details: dict = None

    def load(self, config_path='config.json'):
        config_json_path = os.path.join(DBConfig.current_dir, config_path)
        config_json = json.loads(open(config_json_path, 'r').read())

        DBConfig.bus_journey_details = config_json["db_details"]["bus_journey_details"]
        DBConfig.bus_details = config_json["db_details"]["bus_details"]
        DBConfig.agency_details = config_json["db_details"]["agency_details"]
        DBConfig.agency_user_details = config_json["db_details"]["agency_user_details"]
        DBConfig.journey_seat_details = config_json["db_details"]["journey_seat_details"]
        DBConfig.user_info_details = config_json["db_details"]["user_info_details"]
        DBConfig.user_ticket_details = config_json["db_details"]["user_ticket_details"]
        DBConfig.ticket_payment_details = config_json["db_details"]["ticket_payment_details"]


class AppConfig(Config_Settings_Base, metaclass=SingleInstanceMetaClass):
    app_root_dir: str = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    current_dir: str = os.path.dirname(os.path.abspath(__file__))

    TITLE: str = None
    VERSION: str = None
    DESCRIPTION: str = None
    HOST: str = None
    PORT: int = None
    RELOAD: bool = None
    DEBUG: bool = None
    PUBLIC_URL: str = None
    SERVER_HOST: str = None
    
    def load(self, config_path='config.json'):
        config_json_path = os.path.join(DBConfig.current_dir, config_path)
        config_json = json.loads(open(config_json_path, 'r').read())

        json_dict = config_json["app_details"]

        AppConfig.TITLE = get_env_variable("TITLE", json_dict, str)
        AppConfig.VERSION = get_env_variable("VERSION", json_dict, str)
        AppConfig.DESCRIPTION = get_env_variable("DESCRIPTION", json_dict, str)
        AppConfig.HOST = get_env_variable("HOST", json_dict, str)
        AppConfig.PORT = get_env_variable("PORT", json_dict, int)
        AppConfig.RELOAD = get_env_variable("RELOAD", json_dict, bool)
        AppConfig.DEBUG = get_env_variable("DEBUG", json_dict, bool)
        # use reverse of urllib.parse.urlsplit, i.e. urlunsplit
        # SplitResult(scheme='http', netloc='www.example.com', path='/index', query='', fragment='')
        # it needs a 5 tuple of the above values
        # urlunsplit(('http', 'localhost:5000', '', "",  ""))
        AppConfig.PUBLIC_URL = get_env_variable("PUBLIC_URL", json_dict, str)
        AppConfig.SERVER_HOST = ":".join([str(AppConfig.HOST), str(AppConfig.PORT)])


config_path = 'config.json'
DBConfig().load(config_path)
AppConfig().load(config_path)
