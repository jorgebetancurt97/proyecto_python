from logging import debug, error
from MySQLdb.cursors import Cursor
from flask import Flask,jsonify
from flask.wrappers import Request
from flask_mysqldb import MySQL
from werkzeug.wrappers import request, response  
import json
from flask import Flask, request, Response, json

#m conexion a mysq
app = Flask(__name__)
mysql = MySQL(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'contraseña'
app.config['MYSQL_DB'] = 'service_db'


def establishConnection():
    connection=pymysql.connect(host='localhost',port=)
    cursor=connection.cursor()
    return (connection, cursor)

##listar cursos existentes*
@app.route('/listar', methods=['GET'])
def list():
    conn,cur=establishConnection()
    try:
        cur=mysql.connection.cursor()
        cur.execute('SELECT * FROM registros') 
        data=cur.fetchall()
        listado = []
        for fila in data:
            lista = {'cedula':fila[0], 'nombres':fila[1], 'apellidos':fila[2], 'email':fila[3]}
            listado.append(lista)
        return jsonify({'lista de inscritos': listado, })    

    except Exception as ex:
        return "No se pudo listar" 
    finally:
        conn.close()
        
#listar un curso*
@app.route('/listar/<cedula>', methods=['GET'])
def leer_cedula(cedula):
    try:
        cur=mysql.connection.cursor()
        sql="SELECT * FROM registros WHERE cedula = '{0}' ".format(cedula)
        cur.execute(sql)
        data=cur.fetchone()
        if data != None:
            lista = {'cedula':data[0], 'nombres':data[1], 'apellidos':data[2], 'email':data[3]}
            
            
            return jsonify({'mensaje' : lista })
        else :
            return jsonify({'mensaje': "curso no encontrado", }) 

    except Exception as ex:
        return jsonify({'mensaje': error, })  


@app.route('/agregar',methods=['POST'])
def agregar():
    try:
        cur=mysql.connection.cursor()
        sql="""INSERT INTO registros (cedula, nombres, apellidos ,email )
        VALUES ('{0}','{1}','{2}','{3}') """.format(request.json['cedula'],request.json['nombres'] , request.json['apellidos'], request.json['email'] ) 
        cur.execute(sql)
        mysql.connection.commit()#confirmacion de insercion
        return jsonify({'mensaje': "agregado  correctamente "})  
    
        
    except Exception as ex:
        return jsonify({'mensaje': "error", })   
    
@app.route('/eliminar/<cedula>',methods=['DELETE'])
def eliminar(cedula):
    try:
        cur=mysql.connection.cursor()
        sql="DELETE FROM registros WHERE cedula = '{0}' ".format(cedula)
        cur.execute(sql)
        mysql.connection.commit()#confirmacion de insercion
        return jsonify({'mensaje ': "eliminacion exitosa"})
    
    
    
    except Exception as ex:
        return jsonify({'mesnsaje': "no se pudo eliminar "})
    
@app.route('/actualizar/<cedula>',methods=['PUT'])
def actualizar(cedula):
    try:
        cur=mysql.connection.cursor()
        sql="""UPDATE registros SET nombres = '{0}' , apellidos = '{1}', email = '{2}'
        WHERE cedula '{3}' """.format(request.json['nombres'] , request.json['apellidos'], request.json['email'],cedula ) 
        
        cur.execute(sql)
        mysql.connection.commit()#confirmacion de insercion
        return jsonify({'mensaje': "actualizacion de datos correctamente"})  
        
    
    
    except Exception as ex:
        return jsonify({'mensaje': "error ejecutando la actualizacion" }) 
        
    
        


#seting de comexion
if __name__=='__main__':
    app.run(port=3000 , debug=True )
