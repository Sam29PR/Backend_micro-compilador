import tkinter as tk
from tkinter import filedialog, messagebox

# Suponiendo que tienes una función execute_code en tu backend
try:
    from app import execute_code
except ImportError:
    def execute_code(code):
        return "Simulación de compilación. Resultado:" + code

class CompilerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Micro Compilador - Escritorio")
        self.root.geometry("800x600")

        # Área de entrada de código
        self.code_input = tk.Text(root, height=20, wrap="word", font=("Courier", 12))
        self.code_input.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        # Botones
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Ejecutar", command=self.execute_code).pack(side="left", padx=5)
        tk.Button(button_frame, text="Cargar", command=self.load_file).pack(side="left", padx=5)
        tk.Button(button_frame, text="Guardar", command=self.save_file).pack(side="left", padx=5)

        # Resultado
        self.result_output = tk.Text(root, height=10, wrap="word", bg="#f0f0f0", font=("Courier", 11))
        self.result_output.pack(fill="both", expand=True, padx=10, pady=(5, 10))

    def execute_code(self):
        code = self.code_input.get("1.0", tk.END)
        try:
            result = execute_code(code)
        except Exception as e:
            result = f"⚠️ Error: {e}"
        self.result_output.delete("1.0", tk.END)
        self.result_output.insert(tk.END, result)

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Archivos .txt o .mc", "*.txt *.mc")])
        if path:
            with open(path, "r", encoding="utf-8") as file:
                self.code_input.delete("1.0", tk.END)
                self.code_input.insert(tk.END, file.read())

    def save_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".mc")
        if path:
            with open(path, "w", encoding="utf-8") as file:
                file.write(self.code_input.get("1.0", tk.END))
            messagebox.showinfo("Guardado", f"Guardado en {path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CompilerApp(root)
    root.mainloop()
