import tkinter as tk
from tkinter import messagebox, Toplevel
from conexion import DBConexion


class VentanaPrincipal:
    def __init__(self, master, encriptar_func, verificar_func):
        self.master = master
        self.encriptar = encriptar_func
        self.verificar = verificar_func

        self.master.title("Bcrypt")
        self.master.config(bg="#85929E")
        self.master.resizable(False, False)

        # Tamaño y centrado
        wventana, hventana = 800, 500
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws // 2) - (wventana // 2)
        y = (hs // 2) - (hventana // 2)
        self.master.geometry(f"{wventana}x{hventana}+{x}+{y}")

        # Título principal
        titulo = tk.Label(self.master, text="Bcrypt", bg="#85929E", fg="white", font=("Cambria", 36, "bold"))
        titulo.pack(pady=80)

        # Botones
        self.btn_registrar = tk.Button(
            self.master, text="Registrar Usuario", width=40, bd=3, bg="#D4E6F1",
            font=("Cambria", 12, "bold"), command=self.abrir_registro
        )
        self.btn_registrar.pack(pady=10)

        self.btn_iniciar_sesion = tk.Button(
            self.master, text="Iniciar Sesión", width=40, bd=3, bg="#D4E6F1",
            font=("Cambria", 12, "bold"), command=self.abrir_login
        )
        self.btn_iniciar_sesion.pack(pady=10)

    # ---------- Ventana de registro ----------
    def abrir_registro(self):
        reg_win = Toplevel(self.master)
        reg_win.title("Registrar Usuario")
        reg_win.geometry("400x350")
        reg_win.config(bg="#A9CCE3")
        reg_win.resizable(False, False)
        reg_win.grab_set()

        tk.Label(reg_win, text="Nombre:", bg="#A9CCE3", font=("Cambria", 12)).pack(pady=5)
        nombre_entry = tk.Entry(reg_win, width=40)
        nombre_entry.pack(pady=5)

        tk.Label(reg_win, text="Usuario:", bg="#A9CCE3", font=("Cambria", 12)).pack(pady=5)
        usuario_entry = tk.Entry(reg_win, width=40)
        usuario_entry.pack(pady=5)

        tk.Label(reg_win, text="Contraseña:", bg="#A9CCE3", font=("Cambria", 12)).pack(pady=5)
        frame_pass = tk.Frame(reg_win, bg="#A9CCE3")
        frame_pass.pack(pady=5)

        pass_entry = tk.Entry(frame_pass, show="*", width=34)
        pass_entry.pack(side="left", padx=(0, 5))

        def toggle_password():
            if pass_entry.cget('show') == '':
                pass_entry.config(show='*')
                btn_toggle.config(text='👁️')
            else:
                pass_entry.config(show='')
                btn_toggle.config(text='🙈')

        btn_toggle = tk.Button(frame_pass, text="👁️", width=3, command=toggle_password)
        btn_toggle.pack(side="right")

        def registrar_usuario():
            nombre = nombre_entry.get()
            usuario = usuario_entry.get()
            password = pass_entry.get()

            if not (nombre and usuario and password):
                messagebox.showwarning("Error", "Todos los campos son obligatorios.")
                return

            password_hash = self.encriptar(password)
            db = DBConexion()
            if db.conn:
                exito = db.insertar_usuario(nombre, usuario, password_hash)
                if exito:
                    messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
                    reg_win.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo registrar el usuario.")
            else:
                messagebox.showerror("Error", "Sin conexión a la base de datos.")

        tk.Button(reg_win, text="Registrar", width=20, bg="#D4E6F1", font=("Cambria", 12, "bold"),
                  command=registrar_usuario).pack(pady=20)

    # ---------- Ventana de inicio de sesión ----------
    def abrir_login(self):
        login_win = Toplevel(self.master)
        login_win.title("Iniciar Sesión")
        login_win.geometry("400x300")
        login_win.config(bg="#A9CCE3")
        login_win.resizable(False, False)
        login_win.grab_set()

        tk.Label(login_win, text="Usuario:", bg="#A9CCE3", font=("Cambria", 12)).pack(pady=5)
        usuario_entry = tk.Entry(login_win, width=40)
        usuario_entry.pack(pady=5)

        tk.Label(login_win, text="Contraseña:", bg="#A9CCE3", font=("Cambria", 12)).pack(pady=5)
        frame_pass = tk.Frame(login_win, bg="#A9CCE3")
        frame_pass.pack(pady=5)

        pass_entry = tk.Entry(frame_pass, show="*", width=34)
        pass_entry.pack(side="left", padx=(0, 5))

        def toggle_password():
            if pass_entry.cget('show') == '':
                pass_entry.config(show='*')
                btn_toggle.config(text='👁️')
            else:
                pass_entry.config(show='')
                btn_toggle.config(text='🙈')

        btn_toggle = tk.Button(frame_pass, text="👁️", width=3, command=toggle_password)
        btn_toggle.pack(side="right")

        def verificar_usuario():
            usuario = usuario_entry.get()
            password = pass_entry.get()

            if not (usuario and password):
                messagebox.showwarning("Error", "Todos los campos son obligatorios.")
                return

            exito, nombre = self.verificar(usuario, password)
            if exito:
                messagebox.showinfo("Bienvenido", f"Bienvenido, {nombre}")
                login_win.destroy()
                self.mostrar_bienvenida(nombre, usuario)
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

        tk.Button(login_win, text="Iniciar Sesión", width=20, bg="#D4E6F1", font=("Cambria", 12, "bold"),
                  command=verificar_usuario).pack(pady=20)

    # ---------- Ventana de bienvenida ----------
    def mostrar_bienvenida(self, nombre, usuario):
        bienvenida = Toplevel(self.master)
        bienvenida.title("Bienvenida")
        bienvenida.geometry("400x200")
        bienvenida.config(bg="#82E0AA")
        bienvenida.resizable(False, False)
        bienvenida.grab_set()
        #Etiquetas de bienvenida
        tk.Label(bienvenida, text=f"Nombre: {nombre}", bg="#82E0AA", fg="black",
                 font=("Cambria", 16)).pack(expand=True)
        tk.Label(bienvenida, text=f"Usuario: {usuario}", bg="#82E0AA", fg="black",
                 font=("Cambria", 16)).pack(expand=True)

