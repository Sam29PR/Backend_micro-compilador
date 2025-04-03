from flask import Flask, request, jsonify
from flask_cors import CORS
from compiler import get_tokens, parse_code, execute_code  
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})  

# Carpeta donde se guardarán los archivos
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FILES_DIR = os.path.join(BASE_DIR, "files")
os.makedirs(FILES_DIR, exist_ok=True)  # Crear la carpeta si no existe

@app.route("/tokens", methods=["POST"])
def analyze_tokens():
    data = request.get_json()
    code = data.get("code", "")
    tokens = get_tokens(code)
    return jsonify({"tokens": tokens})

@app.route("/compile", methods=["POST"])
def compile_code():
    data = request.get_json()
    code = data.get("code", "")
    print("codigo reicibido: ",code)

    syntax_tree, errors = parse_code(code)

    if errors:
        return jsonify({"error": errors})

    output = execute_code(syntax_tree)  
    return jsonify({"output": output})

# ✅ Nuevo Archivo (Simplemente limpia el editor)
@app.route("/new-file", methods=["POST"])
def new_file():
    return jsonify({"message": "Nuevo archivo listo para escribir.", "content": ""})

# ✅ Abrir Archivo (Cargar contenido desde un archivo)
@app.route("/open-file", methods=["POST"])
def open_file():
    data = request.json
    filename = data.get("filename")
    file_path = os.path.join(FILES_DIR, filename)

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return jsonify({"message": f"Archivo {filename} cargado.", "content": content})
    else:
        return jsonify({"error": "Archivo no encontrado"}), 404

# ✅ Eliminar Archivo
@app.route("/delete-file", methods=["POST"])
def delete_file():
    data = request.json
    filename = data.get("filename")
    file_path = os.path.join(FILES_DIR, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"message": f"Archivo {filename} eliminado correctamente."})
    else:
        return jsonify({"error": "Archivo no encontrado"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
