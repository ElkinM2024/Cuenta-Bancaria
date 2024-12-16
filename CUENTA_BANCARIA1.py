import tkinter as tk
from tkinter import messagebox

class CuentaBancaria:
    def __init__(self, numero_cuenta, titular, saldo, tipo_cuenta):
        self.numero_cuenta = numero_cuenta
        self.titular = titular
        self.saldo = saldo
        self.tipo_cuenta = tipo_cuenta
        self.historial = []

    def consultar_saldo(self):
        return self.saldo

    def depositar(self, monto):
        if monto <= 0:
            return "El monto a depositar debe ser mayor que cero."
        self.saldo += monto
        self.historial.append(f"Depósito: {monto}")
        return f"Depósito exitoso. Saldo actual: {self.saldo}"

    def retirar(self, monto):
        if monto <= 0:
            return "El monto a retirar debe ser mayor que cero."
        if monto > self.saldo:
            return "Saldo insuficiente para realizar el retiro."
        self.saldo -= monto
        self.historial.append(f"Retiro: {monto}")
        return f"Retiro exitoso. Saldo actual: {self.saldo}"

    def transferir(self, cuenta_destino, monto):
        if monto <= 0:
            return "El monto a transferir debe ser mayor que cero."
        if monto > self.saldo:
            return "Saldo insuficiente para realizar la transferencia."
        if not isinstance(cuenta_destino, CuentaBancaria):
            return "Cuenta de destino no válida."
        self.saldo -= monto
        cuenta_destino.saldo += monto
        self.historial.append(f"Transferencia: {monto} a cuenta {cuenta_destino.numero_cuenta}")
        cuenta_destino.historial.append(f"Transferencia recibida: {monto} de cuenta {self.numero_cuenta}")
        return f"Transferencia de {monto} a cuenta {cuenta_destino.numero_cuenta} realizada con éxito."

    def mostrar_historial(self):
        if not self.historial:
            return "No se han realizado transacciones."
        return "\n".join(self.historial)


class BancoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Cuenta Bancaria")
        self.root.geometry("600x600")
        self.root.config(bg="#F2F2F2")  # Fondo general suave

        # Crear las cuentas de ejemplo
        self.cuenta1 = CuentaBancaria("001", "Juan Pérez", 1000, "Ahorros")
        self.cuenta2 = CuentaBancaria("002", "Ana López", 500, "Corriente")

        self.create_widgets()

    def create_widgets(self):
        # Fondo con gradiente (declaramos un frame que actúa como fondo)
        self.frame_fondo = tk.Frame(self.root, bg="#1E90FF", bd=10, relief="sunken", padx=20, pady=20)
        self.frame_fondo.pack(padx=20, pady=20, fill="both", expand=True)

        # Título centralizado
        self.titulo_label = tk.Label(self.frame_fondo, text="Simulación de Cuenta Bancaria", font=("Helvetica", 18, "bold"), bg="#1E90FF", fg="white")
        self.titulo_label.pack(pady=10)

        # Saldo
        self.saldo_label = tk.Label(self.frame_fondo, text=f"Saldo: {self.cuenta1.consultar_saldo()} €", font=("Arial", 16), bg="#1E90FF", fg="#FFF")
        self.saldo_label.pack(pady=20)

        # Campo para monto
        self.monto_label = tk.Label(self.frame_fondo, text="Monto:", font=("Arial", 12), bg="#1E90FF", fg="#FFF")
        self.monto_label.pack()
        self.monto_entry = tk.Entry(self.frame_fondo, font=("Arial", 14), bg="#fff", fg="#333", bd=2, relief="solid", width=20)
        self.monto_entry.pack(pady=10)

        # Botones mejorados
        self.depositar_button = self.create_button("Depositar", "#32CD32", self.depositar)
        self.retirar_button = self.create_button("Retirar", "#FF6347", self.retirar)
        self.transferir_button = self.create_button("Transferir", "#FFD700", self.transferir)
        self.historial_button = self.create_button("Historial", "#4682B4", self.mostrar_historial)
        self.salir_button = self.create_button("Salir", "#B22222", self.root.quit)

        # Empaquetar botones
        self.depositar_button.pack(pady=5, fill="x")
        self.retirar_button.pack(pady=5, fill="x")
        self.transferir_button.pack(pady=5, fill="x")
        self.historial_button.pack(pady=5, fill="x")
        self.salir_button.pack(pady=5, fill="x")

    def create_button(self, text, color, command):
        """Crear botones con colores personalizados y estilo atractivo"""
        button = tk.Button(self.frame_fondo, text=text, font=("Arial", 14), bg=color, fg="white", relief="flat", command=command, height=2)
        button.config(activebackground="#005f4f", activeforeground="white")
        button.bind("<Enter>", lambda event, btn=button: btn.config(bg="#006400"))  # Hover efecto
        button.bind("<Leave>", lambda event, btn=button: btn.config(bg=color))  # Volver al color original
        return button

    def depositar(self):
        try:
            monto = float(self.monto_entry.get())
            if monto <= 0:
                messagebox.showerror("Error", "El monto debe ser mayor que cero.")
            else:
                mensaje = self.cuenta1.depositar(monto)
                self.saldo_label.config(text=f"Saldo: {self.cuenta1.consultar_saldo()} €")
                messagebox.showinfo("Depósito Exitoso", mensaje)
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto válido.")

    def retirar(self):
        try:
            monto = float(self.monto_entry.get())
            if monto <= 0:
                messagebox.showerror("Error", "El monto debe ser mayor que cero.")
            else:
                mensaje = self.cuenta1.retirar(monto)
                self.saldo_label.config(text=f"Saldo: {self.cuenta1.consultar_saldo()} €")
                messagebox.showinfo("Retiro Exitoso", mensaje)
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto válido.")

    def transferir(self):
        try:
            monto = float(self.monto_entry.get())
            if monto <= 0:
                messagebox.showerror("Error", "El monto debe ser mayor que cero.")
            else:
                mensaje = self.cuenta1.transferir(self.cuenta2, monto)
                self.saldo_label.config(text=f"Saldo: {self.cuenta1.consultar_saldo()} €")
                messagebox.showinfo("Transferencia Exitosa", mensaje)
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto válido.")

    def mostrar_historial(self):
        historial = self.cuenta1.mostrar_historial()
        messagebox.showinfo("Historial de Transacciones", historial)


if __name__ == "__main__":
    root = tk.Tk()
    app = BancoApp(root)
    root.mainloop()
