from dbInterface import DBInterface
from app import login_manager
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, login, password):
        self.id = id
        self.login = login
        self.password = password


@login_manager.user_loader
def load_user(id):
    try:
        db = DBInterface()

        login, password = db.getUserLogPassByID(id)

        return User(id, login, password)
    except:
        return None
