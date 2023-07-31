import os
import sqlite3
from sqlite3 import Error

class manager_db():
    def __init__(self):
        self.TIMER = 30
        self.DB_path = './db/Manager.db'

        # Verificar si la base de datos existe antes de conectarse
        if not os.path.exists(self.DB_path):
            self.crear_base_de_datos()
        else:
            # Conectar con la base de datos
            self.conn = sqlite3.connect(self.DB_path)
            self.cur = self.conn.cursor()

        # Crear tabla si no existe
        self.crear_tabla()

    ##################################################################
    ### Metodos

    def crear_base_de_datos(self):
        self.conn = sqlite3.connect(self.DB_path)
        self.cur = self.conn.cursor()
        # Crea la tabla después de conectarse a la base de datos
        self.crear_tabla()

    def crear_tabla(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS to_render 
            (comando TEXT UNIQUE NOT NULL)
        ''')

    def leer_datos(self):
        try:
            # Ejecuta una consulta para obtener todos los registros de la tabla
            self.cur.execute("SELECT * FROM to_render")
            records = self.cur.fetchall()
            result = [item[0] for item in records]
            print('result: ', result)
            return result
        finally:
            # Cierra la conexión a la base de datos
            self.conn.close()
