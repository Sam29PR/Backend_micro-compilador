from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMainWindow
)
from PySide6.QtGui import QFont


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("Micro Compilador")
        MainWindow.resize(800, 600)

        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        # Layout principal vertical
        self.layout = QVBoxLayout(self.centralwidget)

        # Etiqueta de entrada
        self.labelCodigo = QLabel("Código fuente:")
        self.labelCodigo.setFont(QFont("Arial", 12, QFont.Bold))
        self.layout.addWidget(self.labelCodigo)

        # Área de entrada de código
        self.txtCodigo = QTextEdit()
        self.txtCodigo.setFont(QFont("Courier", 11))
        self.layout.addWidget(self.txtCodigo)

        # Botón Ejecutar
        self.btnEjecutar = QPushButton("Ejecutar")
        self.layout.addWidget(self.btnEjecutar)

        # Etiqueta de salida
        self.labelSalida = QLabel("Salida del compilador:")
        self.labelSalida.setFont(QFont("Arial", 12, QFont.Bold))
        self.layout.addWidget(self.labelSalida)

        # Área de salida
        self.txtSalida = QTextEdit()
        self.txtSalida.setFont(QFont("Courier", 11))
        self.txtSalida.setReadOnly(True)
        self.layout.addWidget(self.txtSalida)
