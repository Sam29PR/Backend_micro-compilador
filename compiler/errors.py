class CompilationError(Exception):
    def __init__(self, message):
        super().__init__(f"Error de Compilación: {message}")
