from flask import Flask, render_template, request, redirect, url_for
import openpyxl
import os
from confiDB import *

app = Flask(__name__)

@app.route ('/')
def Index():
    return render_template('index.html')

@app.route("/tabla")
def tabla():
    conexion_MySQLdb = connectionBD ()
    cur = conexion_MySQLdb.cursor()
    cur.execute('SELECT * FROM partidos')
    data = cur.fetchall()
    return render_template("tabla.html", partido = data)

@app.route ('/uploads',  methods=['POST'])
def upload():
    conexion_MySQLdb = connectionBD ()
    file = request.files['file_excel']
    file_path = os.path.join ('uploads', file.filename)
    file.save(file_path)
    
    excel_dataframe = openpyxl.load_workbook(file_path)
    dataframe = excel_dataframe.active

    data = []

    cur = conexion_MySQLdb.cursor()

    for row in dataframe.iter_rows(min_row=2, values_only=True):
        data.append(list(row))  

    for fila in data:
        cur.execute(
                    '''
                    INSERT INTO partidos (hora, equipoLocal, equipoVisitante, categoria, cancha, fecha)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ''',tuple(fila))
        conexion_MySQLdb.commit()

    cur.close()
    conexion_MySQLdb.close()
    return redirect(url_for('Index')) 

@app.route("/partido/<id>")
def detalles(id):
    conexion_Mysqldb = connectionBD()
    cur = conexion_Mysqldb.cursor()
    cur.execute ("SELECT * FROM partidos WHERE id = %s", (id,))
    partidos = cur.fetchall()
    return render_template("partido.html", partido = partidos)

@app.route("/buscar_partidos", methods=['POST'])
def buscarPartidos ():
    if request.method == 'POST':
        buscador = request.form['buscar']
        conexion_MySQLdb = connectionBD()
        cur = conexion_MySQLdb.cursor(dictionary=True)
        query =  """
                SELECT * FROM partidos 
                WHERE equipoLocal LIKE %s 
                OR equipoVisitante LIKE %s
                OR categoria LIKE %s
                """
        cur.execute(query,('%' + buscador + '%', '%' + buscador + '%', '%' + buscador + '%'))
 
        partido = cur.fetchall()
        cur.close()
        conexion_MySQLdb.close ()
        return render_template ("ResultadoBusqueda.html", resul = partido, busqueda = buscador)
    return redirect(url_for('Index'))
                           



if __name__ == '__main__':
    app.run(port=8000, debug = True)