from dao.user import UserDAO
from service.auth import AuthService
from service.user import UserService
from setup_db import db

user_dao = UserDAO(session=db.session)

user_service = UserService(dao=user_dao)
auth_service = AuthService(user_service=user_service)
