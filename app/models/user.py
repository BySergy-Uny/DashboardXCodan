from flask_login import UserMixin



class User(UserMixin):
    def __init__(self,id=0, name="Pruebas", email="pruebas@gmail.com", token="pruebas", is_admin=False):
        self.id = id
        self.name = name
        self.email = email
        self.password = token
        self.is_admin = is_admin
    
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False