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
        return Response(response=json.dumps (data))
        
    
    except Exception as e:
        return "No se pudo listar" 
    finally:
       conn.close()        
#listar un curso*
@app.route('/listar/<cedula>', methods=['GET'])
def leer_cedula(cedula):
    conn,cursor=establishConnection()
    try:
        
        sql=("SELECT * FROM registros WHERE cedula = %s")
        cursor.execute(sql,(cedula))
        uno=cursor.fetchone()
        return Response(response=json.dumps (uno))
        

    except Exception as e:
        return "usuario no encontrado" 
    finally:
       conn.close()  


@app.route('/agregar',methods=['POST'])
def agregar():
    conn,cursor=establishConnection()
    try:
        
        sql=("INSERT INTO registros (cedula, nombres, apellidos ,email ) VALUES (%s,%s,%s,%s) ")
        cursor.execute(sql,(request.json['cedula'],request.json['nombres'],request.json['apellidos'],request.json['email'])) 
        
        
        conn.commit()#confirmacion de insercion
        return "adicion de informacion exitosa"
    
    except Exception as e:
        return "no se logro agregar contacto ingresado"  
    finally:
       conn.close()       
    
@app.route('/eliminar/<cedula>',methods=['DELETE'])
def eliminar(cedula):
    conn,cursor=establishConnection()
    try:
        
        sql="DELETE FROM registros WHERE cedula=%s "
        cursor.execute(sql,(cedula))
        conn.commit()#confirmacion de insercion
        return "eliminacion exitosa"
    
    
    
    except Exception as ex:
        return  "no se pudo eliminar "
    finally:
       conn.close()  
       

#seting de comexion
if __name__=='__main__':
    app.run(port=3000 , debug=True )
