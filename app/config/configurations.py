import json
import os
from typing import List
from app.utils.helpers import SingleInstanceMetaClass, get_env_variable


class DBConfig(metaclass=SingleInstanceMetaClass):
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

    def load_configurations(self, config_path='config.json'):
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


class AppConfig(metaclass=SingleInstanceMetaClass):
    app_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    current_dir = os.path.dirname(os.path.abspath(__file__))

    TITLE: str
    VERSION: str
    DESCRIPTION: str
    HOST: str
    PORT: int
    RELOAD: bool
    DEBUG: str

    def load_configurations(self, config_path='config.json'):
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

    @classmethod
    def print(self):
        app_config = \
        f"""
        AppConfig
        {"-"*50}
        TITLE: {AppConfig.TITLE}
        VERSION: {AppConfig.VERSION}
        DESCRIPTION: {AppConfig.DESCRIPTION}
        HOST: {AppConfig.HOST}
        PORT: {AppConfig.PORT}
        RELOAD: {AppConfig.RELOAD}
        DEBUG: {AppConfig.DEBUG}
        {"-"*50}
        """
        return app_config


config_path = 'config.json'
DBConfig().load_configurations(config_path)
AppConfig().load_configurations(config_path)
