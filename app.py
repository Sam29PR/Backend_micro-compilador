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
        execution_state['total_steps'] = len(execution_state['ast'][1]) if execution_state['ast'] else 0
        execution_state['code'] = code
        execution_state['is_running'] = False
        return jsonify({
            "message": result,
            "total_steps": execution_state['total_steps']
        }), 200

@app.route("/execute", methods=["POST"])
def execute():
    code = request.json.get("code", "")
    
    # Validación básica
    if not code.strip():
        return jsonify({"error": "Código vacío"}), 400

    # Compilación inicial
    compile_result = parse_code(code)
    if isinstance(compile_result, list):
        return jsonify({"error": compile_result}), 400
    
    # Configura estado
    execution_state['ast'] = parser.parse(code)
    execution_state['memory'] = {}
    execution_state['current_step'] = 0
    execution_state['total_steps'] = len(execution_state['ast'][1])
    execution_state['code'] = code
    execution_state['is_running'] = True
    
    # Ejecución completa
    try:
        output = execute_code(execution_state['ast'][1], execution_state['memory'].copy())
        return jsonify({
            "status": "completed",
            "output": output,
            "variables": execution_state['memory'],
            "total_steps": execution_state['total_steps']
        })
    except Exception as e:
        execution_state['is_running'] = False
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route("/execute-step", methods=["POST"])
def execute_step():
    # Verifica si hay una ejecución en curso
    if not execution_state['is_running'] and execution_state['ast'] is None:
        return jsonify({
            "status": "error",
            "error": "No hay ejecución en curso. Compila primero."
        }), 400

    execution_state['is_running'] = True
    
    # Verifica si ha terminado
    if execution_state['current_step'] >= execution_state['total_steps']:
        execution_state['is_running'] = False
        return jsonify({
            "status": "completed",
            "output": "",
            "variables": execution_state['memory']
        })
    
    # Ejecuta el paso actual
    try:
        statement = execution_state['ast'][1][execution_state['current_step']]
        output = execute_code([statement], execution_state['memory'].copy())
        
        # Prepara respuesta
        response = {
            "status": "in-progress",
            "current_step": execution_state['current_step'] + 1,
            "total_steps": execution_state['total_steps'],
            "output": output,
            "variables": execution_state['memory'].copy()
        }
        
        execution_state['current_step'] += 1
        return jsonify(response)
        
    except Exception as e:
        execution_state['is_running'] = False
        return jsonify({
            "status": "error",
            "error": str(e),
            "current_step": execution_state['current_step']
        }), 500

@app.route("/reset-execution", methods=["POST"])
def reset_execution():
    execution_state['ast'] = None
    execution_state['memory'] = {}
    execution_state['current_step'] = 0
    execution_state['total_steps'] = 0
    execution_state['code'] = ''
    execution_state['is_running'] = False
    return jsonify({"message": "Ejecución reiniciada"})

@app.route("/execution-status", methods=["GET"])
def execution_status():
    return jsonify({
        "is_running": execution_state['is_running'],
        "current_step": execution_state['current_step'],
        "total_steps": execution_state['total_steps']
    })
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)