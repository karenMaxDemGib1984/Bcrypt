import mariadb

class DBConexion:
    def __init__(self):
        try:
            self.conn = mariadb.connect(
                user="root",
                password="",
                host="127.0.0.1",
                port=3307,
                database="Prueba"
            )
            self.cursor = self.conn.cursor()
            print("Conexión exitosa a la base de datos.")
        except mariadb.Error as error:
            print(f"Error al conectar a la base de datos: {error}")
            self.conn = None
            self.cursor = None

    def insertar_usuario(self, nombre, usuario, password_hash):
        try:
            self.cursor.execute(
                "INSERT INTO usuarios (nombre, usuario, contraseña) VALUES (?, ?, ?)",
                (nombre, usuario, password_hash.decode('utf-8'))
            )
            self.conn.commit()
            return True
        except mariadb.Error as e:
            print(f"Error al insertar usuario: {e}")
            return False

    def obtener_usuario(self, usuario):
        try:
            self.cursor.execute(
                "SELECT nombre, usuario, contraseña FROM usuarios WHERE usuario = ?", (usuario,)
            )
            return self.cursor.fetchone()
        except mariadb.Error as e:
            print(f"Error al obtener usuario: {e}")
            return None
