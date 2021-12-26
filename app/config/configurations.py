import json
import os
from typing import List
from app.utils.helpers import SingleInstanceMetaClass


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

    title: str
    version: str
    description: str
    host: str
    port: int
    reload: bool
    
    def load_configurations(self, config_path='config.json'):
        config_json_path = os.path.join(DBConfig.current_dir, config_path)
        config_json = json.loads(open(config_json_path, 'r').read())
        
        AppConfig.title = config_json["app_details"]["title"]
        AppConfig.version = config_json["app_details"]["version"]
        AppConfig.description = config_json["app_details"]["description"]
        AppConfig.host = config_json["app_details"]["host"]
        AppConfig.port = config_json["app_details"]["port"]
        AppConfig.reload = config_json["app_details"]["reload"]


config_path = 'config.json'
DBConfig().load_configurations(config_path)
AppConfig().load_configurations(config_path)
