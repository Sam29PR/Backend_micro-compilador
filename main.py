from PySide6.QtWidgets import QApplication, QMainWindow
from ui_main import Ui_MainWindow
from compiler import execute_code  # función que usarás

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btnEjecutar.clicked.connect(self.ejecutar)

    def ejecutar(self):
        codigo = self.ui.txtCodigo.toPlainText()
        resultado =execute_code(codigo)
        self.ui.txtSalida.setPlainText(resultado)

    def compilar(self, codigo):
        # Aquí iría tu lógica real
        return f"Compilado (simulado):\n{codigo}"

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
