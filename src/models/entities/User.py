from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class User(UserMixin):
    
    def __init__ (self, id_admin, correo, contraseña, usuario="") -> None :
        self.id = id_admin
        self.correo = correo
        self.contraseña = contraseña 
        self.usuario = usuario

    @classmethod
    def check_password(self, hashed_password, contraseña):
        return check_password_hash(hashed_password, contraseña)
    
    
