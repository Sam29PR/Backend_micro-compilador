from flask import Flask, request, jsonify
from flask_cors import CORS
from compiler.lexer import get_tokens
from compiler.parser import parse_code
from compiler.interpreter import execute_code  # si lo usas para la etapa de ejecución

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

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
        return jsonify({"message": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
