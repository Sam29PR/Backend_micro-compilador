from flask import Flask, request, jsonify
from flask_cors import CORS
from compiler.lexer import get_tokens
from compiler.parser import parse_code, parser
from compiler.interpreter import execute_code
import os
from flask import send_file

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

BASE_DIR = os.path.join(os.getcwd(), "archivos")
os.makedirs(BASE_DIR, exist_ok=True)

# Estado global para la ejecución paso a paso
execution_state = {
    'ast': None,
    'memory': {},
    'current_step': 0,
    'code': ''
}

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
    result = parse_code(code)

    if isinstance(result, list):
        return jsonify({"error": result}), 400
    else:
        # Prepara el estado para posible ejecución
        execution_state['ast'] = parser.parse(code)
        execution_state['memory'] = {}
        execution_state['current_step'] = 0
        execution_state['code'] = code
        return jsonify({"message": result}), 200

@app.route("/execute", methods=["POST"])
def execute():
    # Primero compila el código
    code = request.json.get("code", "")
    compile_result = parse_code(code)
    
    if isinstance(compile_result, list):
        return jsonify({"error": compile_result}), 400
    
    # Prepara el estado de ejecución
    execution_state['ast'] = parser.parse(code)
    execution_state['memory'] = {}
    execution_state['current_step'] = 0
    execution_state['code'] = code
    
    # Ejecuta todo de una vez (modo normal)
    output = execute_code(execution_state['ast'][1], execution_state['memory'].copy())
    
    return jsonify({
        "message": "Ejecución completada",
        "output": output,
        "variables": execution_state['memory']
    })

@app.route("/execute-step", methods=["POST"])
def execute_step():
    if not execution_state['ast'] or execution_state['current_step'] >= len(execution_state['ast'][1]):
        return jsonify({
            "status": "completed",
            "message": "Ejecución finalizada",
            "output": "",
            "variables": {}
        })
    
    # Ejecuta solo el paso actual
    statement = execution_state['ast'][1][execution_state['current_step']]
    output = execute_code([statement], execution_state['memory'].copy())
    
    # Prepara la respuesta
    response = {
        "status": "in-progress",
        "current_step": execution_state['current_step'],
        "total_steps": len(execution_state['ast'][1]),
        "output": output,
        "variables": execution_state['memory'].copy()
    }
    
    execution_state['current_step'] += 1
    
    return jsonify(response)

@app.route("/reset-execution", methods=["POST"])
def reset_execution():
    execution_state['ast'] = None
    execution_state['memory'] = {}
    execution_state['current_step'] = 0
    execution_state['code'] = ''
    return jsonify({"message": "Estado de ejecución reiniciado"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)