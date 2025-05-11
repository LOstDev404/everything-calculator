import re
from flask import jsonify
from sympy import Eq, symbols, solve, sympify
from python.utils import float_to_fraction_percent

def algebra2step_solve(data):
    try:
        if 'algebra2stepequation' not in data:
            return jsonify({'error': 'Missing equation in request data'})

        equation = data['algebra2stepequation']

        equation = normalize_equation(equation)
        if equation.count('=') != 1:
            return jsonify({'error': 'Equation must contain exactly one equal sign (=)'})

        variable_match = re.findall(r'[a-z]', equation)
        if not variable_match:
            return jsonify({'error': 'No variable found in equation'})

        unique_vars = set(variable_match)
        if len(unique_vars) > 1:
            return jsonify({'error': 'Please only use one variable'})

        original_var = variable_match[0]
        equation = equation.replace(original_var, 'x')
        equation = format_for_sympy(equation)
        x = symbols('x')
        lhs_str, rhs_str = equation.split('=')

        try:
            lhs_expr = sympify(lhs_str, evaluate=False)
            rhs_expr = sympify(rhs_str, evaluate=False)

            lhs_expr = lhs_expr.doit()
            rhs_expr = rhs_expr.doit()

            equation_obj = Eq(lhs_expr, rhs_expr)
            solution = solve(equation_obj, x)
        except Exception as e:
            return jsonify({'error': f'Error parsing equation: {str(e)}'})

        if not solution:
            return jsonify({
                'values': {
                    'solution': 'No solution exists',
                }
            })
        formatted_solution = format_solution(solution[0], original_var)
        formatted_solution = formatted_solution.replace('sqrt', '√')
        formatted_solution = formatted_solution.replace('*', '')
        return jsonify({
            'values': {
                'solution': formatted_solution,
            }
        })

    except Exception as e:
        return jsonify({'error': f'Error solving equation: {str(e)}'})

def normalize_equation(equation):
    replacements = {
        '–': '-',    # en dash
        '—': '-',    # em dash
        '−': '-',    # minus sign
        '‐': '-',    # hyphen
        ' ': '',     # spaces
        '\u200b': '', # zero-width space
        '\u00A0': '', # non-breaking space
    }

    result = equation.lower()
    for old, new in replacements.items():
        result = result.replace(old, new)

    return result

def format_for_sympy(equation):
    equation = re.sub(r'(\d)([xX])', r'\1*\2', equation)
    equation = re.sub(r'(\d)(\()', r'\1*\2', equation)
    equation = re.sub(r'(\))(\()', r'\1*\2', equation)
    equation = re.sub(r'(\))(\d)', r'\1*\2', equation)
    equation = re.sub(r'([xX])(\d+)', r'\2*\1', equation)

    return equation

def format_solution(solution, variable):
    solution_str = str(solution)
    if ('(' in solution_str or ')' in solution_str or 
        '+' in solution_str or '*' in solution_str) and '/' in solution_str:
        return f"{variable} = {solution_str}"
    if '/' in solution_str:
        try:
            if solution_str.count('/') == 1:
                numerator, denominator = solution_str.split('/')
                numerator = numerator.strip('()')
                denominator = denominator.strip('()')
                decimal_value = float(numerator) / float(denominator)
                return f"{variable} = {float_to_fraction_percent(decimal_value, '', False, False)}"
            else:
                decimal_value = float(eval(solution_str))
                return f"{variable} = {float_to_fraction_percent(decimal_value, '', False, False)}"
        except (ValueError, SyntaxError, NameError):
            return f"{variable} = {solution_str}"
    if solution_str.startswith('-'):
        try:
            decimal_value = float(solution_str)
            return f"{variable} = {float_to_fraction_percent(decimal_value, '', False, False)}"
        except ValueError:
            return f"{variable} = {solution_str}"

    try:
        decimal_value = float(solution_str)
        return f"{variable} = {float_to_fraction_percent(decimal_value, '', False, False)}"
    except ValueError:
        return f"{variable} = {solution_str}"