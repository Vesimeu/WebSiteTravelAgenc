class UserLogin():
    def fromDb(self, user_id, db):
        self.__user = db.getUserInfo(user_id)

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user[0][0])
