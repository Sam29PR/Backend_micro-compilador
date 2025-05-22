def evaluate_expression(expr, memory):
    if isinstance(expr, int):  # Número literal
        return expr
    elif isinstance(expr, str):  # Variable (en desuso si usas 'var')
        return memory.get(expr, 0)
    elif isinstance(expr, tuple):
        # Casos de número o variable
        if expr[0] == 'var':
            return memory.get(expr[1], 0)
        elif expr[0] == 'num':
            return expr[1]

        op = expr[0]

        # Lógica unaria: not
        if op == 'not':
            return not evaluate_expression(expr[1], memory)

        # Lógica binaria
        left = evaluate_expression(expr[1], memory)
        right = evaluate_expression(expr[2], memory)

        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right if right != 0 else 0

        # Operadores relacionales
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

        # Operadores lógicos
        elif op == 'and':
            return bool(left) and bool(right)
        elif op == 'or':
            return bool(left) or bool(right)

    return 0


def execute_code(ast, memory=None):
    if memory is None:
        memory = {}

    output = []

    for statement in ast:
        if statement[0] == 'write':
           # Manejo de múltiples argumentos en write
            parts = []
            for arg in statement[1:]:
                if isinstance(arg, tuple) and arg[0] == 'string':
                    parts.append(arg[1].strip('"'))
                else:
                    evaluated = evaluate_expression(arg, memory)
                    parts.append(str(evaluated))
            output.append(" ".join(parts))

        elif statement[0] == 'assign':
            memory[statement[1]] = evaluate_expression(statement[2], memory)

        elif statement[0] == 'capture':
            var_name = statement[1]
            user_input = input(f"Ingrese un valor para {var_name}: ")
            try:
                memory[var_name] = int(user_input)
            except ValueError:
                memory[var_name] = user_input

        elif statement[0] == 'if':
            condition = evaluate_expression(statement[1], memory)
            if condition:
                new_memory = memory.copy()
                output.extend(execute_code(statement[2], new_memory))

        elif statement[0] == 'while':
            condition = evaluate_expression(statement[1], memory)
            while condition:
                # Crear un nuevo ámbito para cada iteración
                iteration_memory = memory.copy()
                output.extend(execute_code(statement[2], iteration_memory))
                # Actualizar la memoria principal con los cambios de la iteración
                for var in iteration_memory:
                    if var in memory:
                        memory[var] = iteration_memory[var]
                condition = evaluate_expression(statement[1], memory)
                
        elif statement[0] == 'if-else':
            condition = evaluate_expression(statement[1], memory)
            if condition:
                output.extend(execute_code(statement[2], memory.copy()))
            else:
                output.extend(execute_code(statement[3], memory.copy()))


    return output
