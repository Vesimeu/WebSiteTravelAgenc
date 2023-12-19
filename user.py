from dbInterface import DBInterface
from app import login_manager
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, login, password, role):
        self.id = id
        self.login = login
        self.password = password
        self.role = role


@login_manager.user_loader
def load_user(id):
    try:
        db = DBInterface()

        login, password, role = db.getUserLogPassByID(id)

        return User(id, login, password, role)
    except:
        return None
