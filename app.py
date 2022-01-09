from logging import debug, error
from MySQLdb.cursors import Cursor
from flask import Flask,jsonify
from flask.wrappers import Request
from flask_mysqldb import MySQL
from werkzeug.wrappers import request, response  
import json
from flask import Flask, request, Response, json
import pymysql.cursors 

#m conexion a mysq
app = Flask(__name__)
                                
def establishConnection():
   conn=pymysql.connect(host='localhost', user='root', password='0000', database='service_db', cursorclass=pymysql.cursors.DictCursor)
   cursor=conn.cursor() 
   
   return (conn, cursor)

##listar cursos existentes*
@app.route('/listar', methods=['GET'])
def list():
    conn,cursor=establishConnection()
    try:
        cursor.execute('SELECT * FROM registros') 
        data=cursor.fetchall()
        ##print (data)
        ###return Response.json('data', data) 
        return jsonify({'lista de inscritos': data,} )  
            
    
    except Exception as e:
        return "No se pudo listar" 
    finally:
       conn.close()
    
        
#listar un curso*
@app.route('/listar/<cedula>', methods=['GET'])
def leer_cedula(cedula):
    try:
        conn,cursor=establishConnection()
        cursor.execute("SELECT * FROM registros WHERE cedula = '{0}").format(cedula)
        data=cursor.fetchone()
        print (data)
        return jsonify({'mensaje': data, }) 

    except Exception as e:
        return "usuario no encontrado" 
    finally:
       conn.close()  


@app.route('/agregar',methods=['POST'])
def agregar():
    conn,cursor=establishConnection()
    try:
        sql="""INSERT INTO registros (cedula, nombres, apellidos ,email )
        VALUES ('{0}','{1}','{2}','{3}') """.format(request.json['cedula'],request.json['nombres'] , request.json['apellidos'], request.json['email'] ) 
        cursor.execute(sql)
        cursor.connection.commit()#confirmacion de insercion
        return jsonify({'mensaje': "agregado  correctamente "})  
    
        
    except Exception as ex:
        return jsonify({'mensaje': "error", })   
    
@app.route('/eliminar/<cedula>',methods=['DELETE'])
def eliminar(cedula):
    try:
        conn,cursor=establishConnection()
        sql="DELETE FROM registros WHERE cedula = '{0}' ".format(cedula)
        cursor.execute(sql)
        conn.connection.commit()#confirmacion de insercion
        return jsonify({'mensaje ': "eliminacion exitosa"})
    
    
    
    except Exception as ex:
        return jsonify({'mesnsaje': "no se pudo eliminar "})
    
@app.route('/actualizar/<cedula>',methods=['PUT'])
def actualizar(cedula):
    try:
        conn,cursor=establishConnection()
        sql="""UPDATE registros SET nombres = '{0}' , apellidos = '{1}', email = '{2}'
        WHERE cedula '{3}' """.format(request.json['nombres'] , request.json['apellidos'], request.json['email'],cedula ) 
        
        cursor.execute(sql)
        conn.connection.commit()#confirmacion de insercion
        return jsonify({'mensaje': "actualizacion de datos correctamente"})  
        
    
    
    except Exception as ex:
        return jsonify({'mensaje': "error ejecutando la actualizacion" }) 
        
    
        


#seting de comexion
if __name__=='__main__':
    app.run(port=3000 , debug=True )
