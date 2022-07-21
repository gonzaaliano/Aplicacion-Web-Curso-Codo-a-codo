# IMPORTACION LIBRERIAS FLASK

from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime
import os

app = Flask(__name__, template_folder='../templates')
mysql = MySQL()

# CONEXION A BASE DE DATOS
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Galiano01*'
app.config['MYSQL_DATABASE_DB'] = 'empleados'

UPLOADS = os.path.join('uploads')
app.config['UPLOADS'] = UPLOADS #GUARDAMOS LA RUTA COMO UN VALOR EN LA APP 

mysql.init_app(app)

@app.route('/')
def index():
    conn = mysql.connect()
    cursor = conn.cursor()
    
    sql = "SELECT * FROM empleados;"
    cursor.execute(sql)

    empleados = cursor.fetchall()


    conn.commit()

    return render_template('empleados/index.html', empleados = empleados) 

@app.route('/create')
def create():
    
    return render_template('empleados/create.html')

@app.route('/store', methods=["POST"])
def store():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']

    now = datetime.now()
    print(now)
    tiempo = now.strftime("%Y%H%M%S")
    print(tiempo)

    if _foto.filename != '':
        nuevoNombreFoto = tiempo + '_' + _foto.filename
        _foto.save("uploads/" + nuevoNombreFoto)

    sql = "INSERT INTO empleados (nombre, correo, foto) values (%s, %s, %s);"
    datos = (_nombre, _correo, _foto.filename)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)

    conn.commit()

    return redirect('/')

# RUTA DELETE PARA ELIMINAR EMPLEADOS
@app.route('/delete/<int:id>')
def delete(id):
    sql = "DELETE FROM empleados WHERE id=%s"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, id)
    conn.commit()

    return redirect('/')

# RUTA MODIFY PARA EDITAR NOMBRE, CORREO O FOTO DEL EMPLEADO
@app.route('/modify/<int:id>')
def modify(id):
    sql = "SELECT * FROM empleados WHERE id=%s"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, id)
    empleado = cursor.fetchone()
    conn.commit()

    return render_template('empleados/edit.html', empleado = empleado)


# RUTA UPDATE PARA ACTUALIZAR LA INFORMACION DEL EMPLEADO

@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtNombre']
    _foto = request.form['txtNombre']
    id = request.form['txtId']

    datos = (_nombre, _correo, id)

    conn = mysql.connect()
    cursor = conn.cursor()

    if _foto.filename != '':
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        nuevoNombreFoto = tiempo + '_' + _foto.filename
        _foto.save("uploads/" + nuevoNombreFoto)

    sql = "SELECT foto FROM * empleados WHERE id ={id}"
    cursor.execute(sql)

    nombreFoto = cursor.fetchone()[0]

    os.remove(os.path.join(app.config['UPLOADS'], nombreFoto))


    sql = "UPDATE empleados SET nombre ={_nombre}, _correo = {_correo} WHERE id = {id}"

    datos = (_nombre, _correo, _foto.filename)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)

    conn.commit()





if __name__ == '__main__':
    app.run(debug=True)