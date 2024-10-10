from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_mysqldb import MySQL
import openpyxl
import os
from flask_login import LoginManager, login_user, logout_user, login_required

from config import config

#Models
from models.modelUser import ModelUser

#entities 
from models.entities.User import User

#APP
app = Flask(__name__)
csrf = CSRFProtect()
mysql = MySQL(app)
loguin_manager_app = LoginManager(app)

@loguin_manager_app.user_loader
def load_user (id_admin):
    return ModelUser.get_by_id(mysql, id_admin)




@app.route ('/Index')
@login_required
def Index():
    return render_template('index.html')

#LOGUIN ADMIN - VERIFICACIÓN + LOGUIN

@app.route('/admin', methods= ['GET', 'POST'])
def admin ():
    
    if request.method == 'POST':
        user = User(0, request.form['correo'], request.form['contraseña'])

        usuario_logueado = ModelUser.login(mysql, user)

        if usuario_logueado is not None:  # Si se encontró el usuario
            if usuario_logueado.contraseña:  # Verifica si la contraseña es correcta (llama al método check_password())
                login_user(usuario_logueado)
                return redirect(url_for('Index'))
            
            else:
                flash("Contraseña invalida...")
                return render_template ('login.html')
        # if usuario_loguiado != None :
        #     if usuario_loguiado.check_password:
        #         return redirect(url_for('Index'))
        else:
            flash("User not found...")
            return render_template ('login.html')
    else:
        return render_template ('login.html')
    
#Cerrar Sesion
@app.route ('/logout')
def logout ():
    logout_user()
    return redirect(url_for('tabla'))
    

# MOSTRAR PARTIDOS 

@app.route("/")
def tabla():
    cur = mysql.connection.cursor() #Establecer la variable conexion a la base de datos
    cur.execute('SELECT * FROM partidos') #Ejecutar varibale de conexión
    data = cur.fetchall() #Captar los datos de la tabla
    return render_template("tabla.html", partido = data)



#Cargar datos de excel y guardar en la base de datos

@app.route ('/uploads',  methods=['POST'])
def upload():   
    
    file = request.files['file_excel'] #Recuperar datos del formulario 
    file_path = os.path.join ('uploads', file.filename)
    file.save(file_path)
    
    excel_dataframe = openpyxl.load_workbook(file_path)
    dataframe = excel_dataframe.active

    data = []

    cur = mysql.connection.cursor()

    for row in dataframe.iter_rows(min_row=2, values_only=True):
        data.append(list(row))  

    for fila in data:
        cur.execute(
                    '''
                    INSERT INTO partidos (hora, equipoLocal, equipoVisitante, categoria, cancha, fecha)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ''',tuple(fila))
        mysql.connection.commit()

    cur.close()
    return redirect(url_for('Index')) 


# Mostar detalles de partido por ID

@app.route("/partido/<id>")
def detalles(id):

    cur = mysql.connection.cursor()
    cur.execute ("SELECT * FROM partidos WHERE id = %s", (id,))
    partidos = cur.fetchall()
    return render_template("partido.html", partido = partidos)



@app.route("/buscar_partidos", methods=['POST'])
def buscarPartidos ():
    if request.method == 'POST':
        buscador = request.form['buscar']
        
        cur = mysql.connection.cursor()

        query =  """
                SELECT * FROM partidos 
                WHERE equipoLocal LIKE %s 
                OR equipoVisitante LIKE %s
                OR categoria LIKE %s
                """
        cur.execute(query,('%' + buscador + '%', '%' + buscador + '%', '%' + buscador + '%'))
 
        partido = cur.fetchall()
        cur.close()
        
        return render_template ("ResultadoBusqueda.html", resul = partido, busqueda = buscador)
    return redirect(url_for('Index'))
                           
# Vistas de error
def status_401(error):
    return redirect (url_for('tabla'))

def status_404(error):
    return "<h1>Pagina no encontrada</h1>", 404


# Correr aplicación 

# if __name__ == '__main__':
#     app.run(port=8000, debug = True)

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()    