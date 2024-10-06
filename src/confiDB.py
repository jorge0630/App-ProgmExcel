import mysql.connector

def connectionBD():
    mydb = mysql.connector.connect(
        host ="127.0.0.1",
        user ="root",
        passwd = "",
        database = "programaciones" 
    )
    return mydb

    '''       
    if mydb:
        print ("Conexion exitosa")
    else:
        print ("Error en la conexion a BD")
    '''
