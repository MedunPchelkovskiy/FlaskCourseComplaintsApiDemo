from flask_testing import TestCase
from werkzeug.security import generate_password_hash

from config import create_app
from db import db
from managers.authentication import UserAuthenticationManager
from models import UserModel, RoleType


def generate_token(user):
    return UserAuthenticationManager.encode_token(user)

# def create_user_in_db(role=RoleType.complainer):  # създаването на потребител за нуждите на тестване се заменя от пакета factory_boy, виж файла tests.factory
#     password = '321F!v5'
#     hashed_password = generate_password_hash(password)
#     user = UserModel(first_name='Test', last_name='Test', email='test@test.com', phone='0890123456',
#                      password=hashed_password, iban='1111111111111111111111', role = role)
#     db.session.add(user)
#     db.session.commit()
#     return user


class TestRestApiBase(TestCase):
    def create_app(self):
        return create_app('config.TestingConfig')

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
