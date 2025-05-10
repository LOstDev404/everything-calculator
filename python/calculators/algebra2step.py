import re
from flask import jsonify
from python.utils import float_to_fraction_percent
from sympy import Eq, symbols, solve, sympify

def algebra2step_solve(data):
    try:
        equation = data['algebra2stepequation']
        equation = (
            equation
            .replace('–', '-')  
            .replace('—', '-')  
            .replace('−', '-')   
            .replace('‐', '-')  
            .replace(' ', '')    
            .replace('\u200b', '') 
            .replace('\u00A0', '')  
            .lower()              
        )

        if equation.count('=') != 1:
            result = jsonify({'error': 'Equation must contain exactly one equal sign (=)'})
            return result
        
        equation = equation.replace('=', ',')
        letter_matches = re.findall(r'[a-z]', equation)
        if len(set(letter_matches)) > 1:
            result = jsonify({'error': 'Please only use one variable'})
            return result
        letter_match = re.search(r'[a-z]', equation)
        letter = letter_matches[0] if letter_matches else None
        letter = letter_match.group(0) if letter_match else None
        if letter:
            equation = equation.replace(letter, 'x')
        equation = re.sub(r'([xX])(\d+)', r'\2\1', equation)
        equation = re.sub(r'(\d)([xX(])', r'\1*\2', equation)
        equation = re.sub(r'(\))(\d)', r'\1*\2', equation)
        print(equation)
        x = symbols('x')
        lhs, rhs = equation.split(',')
        lhs_expr = sympify(lhs)
        rhs_expr = sympify(rhs)
        print(rhs_expr)
        print(lhs_expr)
        equation = Eq(lhs_expr, rhs_expr)
        print(equation)
        solution = solve(equation, x)
        
        if not solution:
            result = jsonify({
                'values': {
                    'solution': 'No solution exists',
                }
            })
            return result
        solution = str(solution[0])
        
        if '/' in solution:
            if '(' in solution or ')' in solution or '*' in solution or '+' in solution:
                result = jsonify({
                    'values': {
                        'solution': f'{letter} = {solution}',
                    }
                })
                return result
            else:
            
                val1, val2 = solution.split('/')
                val1 = float(val1)
                val2 = float(val2)
                solution = val1 / val2
                solution = float_to_fraction_percent(solution, '', False, False)
        
        if '-' in solution:
            solution = solution.replace('-', '-')
            solution = float(solution)
            solution = float_to_fraction_percent(solution, '', False, False)
            result = jsonify({
                'values': {
                    'solution': f'{letter} = {solution}',
                }
            })
            return result
            
                
        
        else:
            solution = str(solution[0])
            solution = float(solution)
            solution = float_to_fraction_percent(solution, '', False, False)
        
        
        result = jsonify({
            'values': {
                'solution': f'{letter} = {solution}',
            }
        })
        
        return result
    except Exception as e:
        result = jsonify({'error': str(e)})
        return result