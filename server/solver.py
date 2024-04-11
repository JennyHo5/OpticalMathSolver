from sympy.parsing.latex import parse_latex
import re
import sympy as sp
from sympy import simplify, sympify, Eq, solve, symbols, Expr, Matrix

def parse_latex_matrix(latex_matrix_str):
    pattern = r'\\begin{array}{[clr]*}(.*?)\\end{array}'
    matches = re.findall(pattern, latex_matrix_str, re.DOTALL)
    
    matrices = []
    for match in matches:
        # Splitting rows and individual elements
        rows = match.strip().split(r'\\')
        matrix = [[sympify(element) for element in row.split('&')] for row in rows]
        matrices.append(Matrix(matrix))
    
    return matrices

def detect_and_perform_operation(latex_str):
    pattern = r'\\left\[\\begin{array}{.*?}(.*?)\\end{array}\\right\](\^{\-1})?'

    matches = re.findall(pattern, latex_str, re.DOTALL)

    if not matches:
        raise ValueError("No matrix found in the provided LaTeX string.")

    matrix_latex, is_inverse = matches[0]
    matrix_latex_full = f'\\begin{{array}}{{}}{matrix_latex}\\end{{array}}'
    matrix = parse_latex_matrix(matrix_latex_full)[0]

    if is_inverse:
        print("Inverse operation detected.")
        if matrix.rows != matrix.cols:
            raise ValueError("Only square matrices can be inverted.")
        result = matrix.inv()
    else:
        placeholders = ['MATRIX1', 'MATRIX2']
        
        matrix_contents = re.findall(r'\\begin{array}{.*?}.*?\\end{array}', latex_str, re.DOTALL)
        temp_str = latex_str
        for i, content in enumerate(matrix_contents):
            temp_str = temp_str.replace(content, placeholders[i], 1)
        
        operation = None

        if '+' in temp_str:
            operation = 'add'
        elif '-' in temp_str:
            operation = 'subtract'
        elif placeholders[0] in temp_str and placeholders[1] in temp_str:
            if temp_str.find(placeholders[0]) < temp_str.find(placeholders[1]):
                between_matrices = temp_str[temp_str.find(placeholders[0]) + len(placeholders[0]):temp_str.find(placeholders[1])]
                if '\\times' in between_matrices:
                    print("Multiplication detected between matrices.")
                    operation = 'multiply'
        
        if operation is None:
            raise ValueError("Unsupported operation or incorrect matrix placeholders.")
        
        matrices = parse_latex_matrix(latex_str)

        # Perform the operation 
        if operation == 'add':
            result = matrices[0] + matrices[1]
        elif operation == 'subtract':
            result = matrices[0] - matrices[1]
        elif operation == 'multiply':
            result = matrices[0] * matrices[1]
    
    return result

def solve_math(latex_str):
    # Check for long division first
    long_div_match = re.search(r'(\d+)\s*\\longdiv\s*\{([\d\s]+)\}', latex_str)
    if long_div_match:
        # The first group is the divisor, the second group (with spaces removed) is the dividend
        divisor = int(long_div_match.group(1))
        dividend = int(long_div_match.group(2).replace(' ', ''))
        quotient, remainder = divmod(dividend, divisor)
        print(f"Long division result: {quotient} Remainder: {remainder}")
        return quotient 
    try:
        result_matrix = detect_and_perform_operation(latex_str)

        print("Resulting Matrix:")
        print(result_matrix)
        return result_matrix

    except Exception as e:
        # If the above fails, try to parse and solve as a general expression
        try:
            sym_expr = parse_latex(latex_str)
            if isinstance(sym_expr, Eq):
                return solve(sym_expr, dict=True)
            elif isinstance(sym_expr, Expr):
                return simplify(sym_expr)
            else:
                raise ValueError("Unsupported type of mathematical expression.")
        except Exception as e:
            print("Error encountered during solving:", e)
            return f"Error encountered during solving: {e}"
