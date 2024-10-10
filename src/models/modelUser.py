from .entities.User import User
from config import *

class ModelUser():

    @classmethod
    def login(self, mydb, user):
        
        try:
            cur = mydb.connection.cursor()
            sql =  """SELECT id_admin, correo, contraseña, usuario FROM admin
                        WHERE correo = '{}' """.format(user.correo)
            cur.execute(sql)
            row = cur.fetchone()
            if row !=	None :
                user = User(row[0], row[1], User.check_password(row[2], user.contraseña), row[3])
                return user 
            else:
                return None

        except Exception as ex:
            raise Exception (ex)
        


    @classmethod
    def get_by_id(self, mydb, id_admin):
        
        try:
            cur = mydb.connection.cursor()
            sql = "SELECT id_admin, correo, usuario FROM admin WHERE id_admin = {}" . format(id_admin)
            cur.execute(sql)
            row = cur.fetchone()
            if row !=	None :
                logued_user = User(row[0], row[1], None, row[2])
                return logued_user 
            else:
                return None

        except Exception as ex:
            raise Exception (ex)