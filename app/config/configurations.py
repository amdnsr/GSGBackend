import json
import os
from typing import List
from app.utils.helpers import SingleInstanceMetaClass


class DBConfig(metaclass=SingleInstanceMetaClass):
    app_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    current_dir = os.path.dirname(os.path.abspath(__file__))

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


config_path = 'config.json'
DBConfig().load_configurations(config_path)
