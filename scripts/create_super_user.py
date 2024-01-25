from werkzeug.security import generate_password_hash

from db import db
from models import UserModel, RoleType


def create_super_user(first_name, last_name, email, password, role, phone):
    password = generate_password_hash(password)
    user = UserModel(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        role=RoleType.admin,
        phone=phone
    )
    db.session.add()
    db.session.commit()


if __name__ == '__main__':
    create_super_user()
