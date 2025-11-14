import MySQLdb
import os

def obtener_conexion():
    return MySQLdb.connect(
        host=os.getenv('MYSQL_HOST', 'db'),
        user=os.getenv('MYSQL_USER', 'mopii'),
        passwd=os.getenv('MYSQL_PASSWORD', 'daw'),
        db=os.getenv('MYSQL_DB', 'tienda_forestal'),
        charset='utf8mb4'
    )

def obtener_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM productos;")
    productos = cursor.fetchall()
    conexion.close()
    return productos

