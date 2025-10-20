import tkinter as tk
import bcrypt
from Interfaz import VentanaPrincipal
from conexion import DBConexion

def encriptar_contraseña(contraseña:str, rondas=16) -> bytes:    
    sal = bcrypt.gensalt(rounds=rondas)  
    hash = bcrypt.hashpw(contraseña.encode('utf-8'),sal)    
    print(f"Contraseña: {contraseña} del tipo: {type(contraseña)} caracteres {len(contraseña)}")
    print(f"Sal: {sal} del tipo: {type(sal)} caracteres {len(sal)}")
    print(f"Hash: {hash} del tipo: {type(hash)} caracteres {len(hash)}")    
    return hash


def verificar_contraseña(usuario:str, contraseña:str):
    db = DBConexion()
    if db.conn:
        datos_usuario = db.obtener_usuario(usuario)
        if datos_usuario:
            #Función para verificar la contraseña
            # columnas de la consulta nombre[0], usuario[1], contraseña[2]
            if bcrypt.checkpw(contraseña.encode('utf-8'), datos_usuario[2].encode('utf-8')):
                return True, datos_usuario[0]  
    return False, None

#Funcion principal para cargar lo de la interfaz
def main():
    GUI = tk.Tk()
    #Crea la interfaz usando la clase del archivo Interfaz.py
    app = VentanaPrincipal(GUI, encriptar_contraseña, verificar_contraseña)
    GUI.mainloop()

#Solo se ejecuta si es el archivo principal que se está ejecutando
if __name__ == "__main__":
    main()

#Para activar el entorno virtual
#entornoBcrypt\Scripts\activate