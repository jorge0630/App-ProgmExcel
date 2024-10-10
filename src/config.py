class Config:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'


class DevelopmentConfig(Config):
    MYSQL_HOST = '127.0.0.1'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''  # Cambia esto por tu contraseña de MySQL
    MYSQL_DB = 'programaciones'  # Cambia esto por el nombre de tu base de datos
    DEBUG = True

config = {
    'development': DevelopmentConfig
}
