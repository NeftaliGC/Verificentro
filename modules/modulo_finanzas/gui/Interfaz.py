import tkinter as tk
from tkinter import ttk  

class InterfazFinanzas:
    def __init__(self):
        
        self.root = tk.Tk()
        self.root.title("Verificación de Placa")
        self.root.geometry("400x200")  

        
        self._centrar_ventana()

        
        self._crear_widgets()

    def _centrar_ventana(self):

        self.root.update_idletasks()
        ancho = self.root.winfo_width()
        alto = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f"+{x}+{y}")

    def _crear_widgets(self):

        lbl_instruccion = tk.Label(
            self.root,
            text="Por favor ingrese su placa:",
            font=("Arial", 12)
        )
        lbl_instruccion.pack(pady=10)  

        
        self.entry_placa = ttk.Entry(
            self.root,
            width=20,
            font=("Arial", 12)
        )
        self.entry_placa.pack(pady=5)

        
        btn_verificar = ttk.Button(
            self.root,
            text="Verificar",
            command=self._verificar_placa  # Función a ejecutar al hacer clic
        )
        btn_verificar.pack(pady=15)

    def _verificar_placa(self):
        
        print("Validando", self.entry_placa.get())
        

def ejecutar(self):
    self.root.mainloop()  # Esta línea es esencial