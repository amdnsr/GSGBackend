from app.core.security import get_password_hash
from app.db.mongo_handler import MongoHandlerBase
from app.models.request_response_models import CreateAccountRequest, LoginRequest, UserProfileResponse
from app.service.schema_models.user_details_model import user_details_connection_info, UserDetailsModel


class UserDetailsRetrievalHandler(MongoHandlerBase):
    def __init__(self, mongo_connection_info) -> None:
        super().__init__(mongo_connection_info)

    def get_user_details_by_email(self, email: str):
        self.connection = self.make_connection()
        user = UserDetailsModel.objects(email=email).first()
        self.close_connection()
        if not user:
            return False
        user = UserProfileResponse.parse_obj(user.to_mongo().to_dict())
        return user

    def get_hashed_password(self, email: str):
        self.connection = self.make_connection()
        user = UserDetailsModel.objects(email=email).first()
        self.close_connection()
        if not user:
            return False
        hashed_password = user.hashed_password
        return hashed_password


user_details_retrieval_handler = UserDetailsRetrievalHandler(
    user_details_connection_info)
