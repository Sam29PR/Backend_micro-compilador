def evaluate_expression(expr, memory):
    if isinstance(expr, int):  # Si es un número, retornarlo
        return expr
    elif isinstance(expr, str):  # Si es una variable, buscar su valor
        return memory.get(expr, 0)
    elif isinstance(expr, tuple):  # Si es una operación matemática
        op, left, right = expr
        left = evaluate_expression(left, memory)
        right = evaluate_expression(right, memory)

        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right if right != 0 else 0
        elif op == '<':
            return left < right
        elif op == '>':
            return left > right
        elif op == '<=':
            return left <= right
        elif op == '>=':
            return left >= right
        elif op == '=':
            return left == right
        elif op == '<>':
            return left != right
        elif op == 'and':
            return left and right
        elif op == 'or':
            return left or right

    return 0

def execute_code(ast):
    memory = {}  # Diccionario para almacenar variables
    output = []

    for statement in ast:
        if statement[0] == 'write':
            msg = statement[1] if isinstance(statement[1], str) else evaluate_expression(statement[1], memory)
            output.append(str(msg))

        elif statement[0] == 'assign':
            memory[statement[1]] = evaluate_expression(statement[2], memory)

        elif statement[0] == 'if':  # Soporte para condicionales
            condition = evaluate_expression(statement[1], memory)
            if condition:
                output.extend(execute_code(statement[2]))  # Ejecutar el bloque del `if`

        elif statement[0] == 'capture':  # Soporte para entrada de usuario
            var_name = statement[1]
            user_input = input(f"Ingrese un valor para {var_name}: ")
            try:
                memory[var_name] = int(user_input)  # Intentar convertir a número
            except ValueError:
                memory[var_name] = user_input  # Guardar como texto si no es un número

    return output
