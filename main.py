import tkinter as tk
from Interfaz import VentanaPrincipal
from conexion import DBConexion
import bcrypt

def encriptar_contraseña(contraseña:str, round=16) -> bytes:    
    sal = bcrypt.gensalt(rounds=round)  
    hash = bcrypt.hashpw(contraseña.encode('utf-8'),sal)    
    print(f"Contraseña: {contraseña} del tipo: {type(contraseña)} caracteres {len(contraseña)}")
    print(f"Sal: {sal} del tipo: {type(sal)} caracteres {len(sal)}")
    print(f"Hash: {hash} del tipo: {type(hash)} caracteres {len(hash)}")    
    return hash


def verificar_contraseña(usuario, contraseña):
    db = DBConexion()
    if db.conn:
        datos_usuario = db.obtener_usuario(usuario)
        if datos_usuario:
            #Función para verificar la contraseña
            if bcrypt.checkpw(contraseña.encode('utf-8'), datos_usuario[2].encode('utf-8')):
                return True, datos_usuario[0]  
    return False, None

#Funcion principal para cargar lo de la interfaz
def main():
    root = tk.Tk()
    #Crea la interfaz usando la clase del archivo Interfaz.py
    app = VentanaPrincipal(root, encriptar_contraseña, verificar_contraseña)
    root.mainloop()

if __name__ == "__main__":
    main()

#Para activar el entorno virtual
#entornoBcrypt\Scripts\activate