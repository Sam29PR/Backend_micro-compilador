from flask import Flask, request, jsonify
from flask_cors import CORS
from compiler.lexer import get_tokens
from compiler.parser import parse_code
from compiler.interpreter import execute_code  # si lo usas para la etapa de ejecución
import os
from flask import send_file



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

BASE_DIR = os.path.join(os.getcwd(), "archivos")
os.makedirs(BASE_DIR, exist_ok=True)

@app.route("/create-file", methods=["POST"])
def create_file():
    data = request.json
    filename = data.get("filename", "nuevo.txt")
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, "w") as f:
        f.write("")  # Crea archivo vacío
    return jsonify({"message": f"Archivo '{filename}' creado."})

@app.route("/open-file", methods=["GET"])
def open_file():
    filename = request.args.get("filename", "nuevo.txt")
    filepath = os.path.join(BASE_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "Archivo no encontrado."}), 404
    with open(filepath, "r") as f:
        content = f.read()
    return jsonify({"content": content})

@app.route("/delete-file", methods=["DELETE"])
def delete_file():
    filename = request.args.get("filename", "nuevo.txt")
    filepath = os.path.join(BASE_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({"message": f"Archivo '{filename}' eliminado."})
    else:
        return jsonify({"error": "Archivo no encontrado."}), 404


@app.route("/tokens", methods=["POST"])
def analyze_tokens():
    code = request.json.get("code", "")
    tokens = get_tokens(code)
    return jsonify({"tokens": tokens})

@app.route("/compile", methods=["POST"])
def compile_code():
    code = request.json.get("code", "")

    result = parse_code(code)  # parse_code devuelve o lista de errores o mensaje de éxito

    if isinstance(result, list):
        # Errores de sintaxis
        return jsonify({"error": result}), 400
    else:
        # Compilación exitosa, ahora podrías ejecutar:
        # output = execute_code(ast)  # si parse_code retornara AST
        return jsonify({"message": result}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
