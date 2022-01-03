from mongoengine.connection import connect, disconnect


class MongoHandlerBase:
    def __init__(self, mongo_connection_info) -> None:
        self.mongo_connection_info = mongo_connection_info

    def make_connection(self):
        if self.mongo_connection_info.get('mongo_env') in ["STAGE", "PRODUCTION"]:
            self.connection = connect(
                alias=self.mongo_connection_info.get('alias'),
                db=self.mongo_connection_info.get('db_name'),
                host=self.mongo_connection_info.get('host_name'),
                port=self.mongo_connection_info.get('host_port'),
                username=self.mongo_connection_info.get('username'),
                password=self.mongo_connection_info.get('username'),
            )
        else:
            connect(
                alias=self.mongo_connection_info.get('alias'),
                db=self.mongo_connection_info.get('db_name'),
                host=self.mongo_connection_info.get('host_name'),
                port=self.mongo_connection_info.get('host_port')
            )

    def close_connection(self):
        disconnect(alias=self.mongo_connection_info.get('alias'))
