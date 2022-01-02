from mongoengine import Document
from mongoengine import StringField
from app.config.configurations import DBConfig

db_config = DBConfig()

class UserDetailsModel(Document):
    first_name = StringField(required=True)
    last_name = StringField()
    email = StringField(required=True)
    phone_number = StringField(required=True)
    hashed_password = StringField(required=True)

    meta = {
        'db_alias': db_config.UserDetailsModel["alias"],
        'collection': db_config.UserDetailsModel["collection_name"]
    }


user_details_connection_info = {
    "alias": "UserDetailsModel",
    "host_name": db_config.MONGO_HOST,
    "host_port": db_config.MONGO_PORT,
    "db_name": db_config.UserDetailsModel["db_name"],
    "collection_name": "UserDetailsModel",
    "mongo_env": db_config.MONGO_ENV,
    "username": db_config.MONGO_USERNAME,
    "password": db_config.MONGO_PASSWORD
}


