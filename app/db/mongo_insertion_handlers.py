from app.core.security import get_password_hash
from app.db.mongo_handler import MongoHandlerBase
from app.models.request_response_models import CreateAccountRequest
from app.service.schema_models.user_details_model import user_details_connection_info, UserDetailsModel


class UserDetailsInsertionHandler(MongoHandlerBase):
    def __init__(self, mongo_connection_info) -> None:
        super().__init__(mongo_connection_info)

    def insert(self, user: CreateAccountRequest):
        hashed_password = get_password_hash(user.password)
        user_dict = user.dict()
        user_dict["hashed_password"] = hashed_password

        self.make_connection()

        model_dict = {}
        model_fields = UserDetailsModel._fields_ordered
        for field in model_fields:
            if field in user_dict:
                model_dict[field] = user_dict[field]

        user_model = UserDetailsModel(**model_dict)
        db_obj = user_model.save()
        self.close_connection()
        return db_obj

    def verify_account(self, email: str):
        self.make_connection()
        try:
            UserDetailsModel.objects(email=email).first().update(
                set__is_email_verified=True)
            self.close_connection()
            return True
        except:
            self.close_connection()
            return False

    def delete_account(self, email: str):
        self.make_connection()
        try:
            UserDetailsModel.objects(email=email).first().delete()
            self.close_connection()
            return True
        except:
            self.close_connection()
            return False


user_details_insertion_handler = UserDetailsInsertionHandler(
    user_details_connection_info)
