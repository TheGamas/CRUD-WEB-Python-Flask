import fdb
import os

def cursor():
    return database.cursor()

def commit():
    database.commit()

try:
  current_path = os.getcwd()
  database_path = os.path.join(current_path, 'FirebirdDB.FDB') 

  database = fdb.connect(
      host='localhost', 
      database=database_path, 
      user='SYSDBA', 
      password='putainocente')
  
  print("Conexión exitosa a Firebird")
  
except Exception as e:
  print("Error al conectar a Firebird: ", str(e))


