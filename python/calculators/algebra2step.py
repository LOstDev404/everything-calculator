from python.utils import float_to_fraction_percent
import re
from flask import jsonify

def algebra2step_solve(data):
    try:    
        equation = data['algebra2stepequation']
        equation = equation.replace(' ', '').lower()
    
        if '(' in equation or ')' in equation:
            result = jsonify({'error': 'Parentheses are not supported'})
    
        if '=' not in equation:
            result = jsonify({'error': 'Equation must contain an equals sign'})
    
        if '/' in equation:
            result = jsonify({'error': 'Division and fractions are not supported in this calculator'})
    
        sides = equation.split('=')
        if len(sides) != 2:
            result = jsonify({'error': 'You can only use one equal sign.'})
        left_side, right_side = sides
    
        variables = sorted(set(re.findall(r'[a-z]', equation)))
        if not variables:
            result = jsonify({'error': 'No letters/variables in the equation'})
        if len(variables) > 1:
            result = jsonify({'error': 'This calculator currently supports only one letter/variable'})
        letter = variables[0]
    
        def process_term(term, is_coefficient=False):
            if not term.strip():
                return 1.0 if is_coefficient else 0.0
    
            sign = -1 if term.startswith('-') else 1
            term = term.lstrip('+-')
    
            if not term:
                return sign * (1.0 if is_coefficient else 0.0)
    
            try:
                if is_coefficient:
                    term = term.replace(letter, '').strip()
                    if not term:  
                        return sign * 1.0
                    return sign * float(term) if term else sign * 1.0
    
                if '/' in term:
                    if term == '/': 
                        return sign * (1.0 if is_coefficient else 0.0)
                    num, denom = term.split('/')
                    num = num.strip() or '1'
                    denom = denom.strip() or '1'
                    return sign * float(num) / float(denom)
    
                return sign * float(term)
            except ValueError as e:
                if is_coefficient and term == letter:
                    return sign * 1.0
                raise ValueError(f"Invalid term: {term}")
    
        def process_side(side):
            var_coeff = 0.0
            const = 0.0
    
            if not side.strip():
                return 0.0, 0.0
    
            terms = re.findall(r'[+-]?[^+-]+', '+' + side.strip())
    
            for term in terms:
                term = term.strip()
                if not term:
                    continue
    
                if letter in term:
                    coeff_str = term.replace(letter, '')
                    var_coeff += process_term(coeff_str, True)
                else:
                    const += process_term(term)
    
            return var_coeff, const
    
        try:
            left_var, left_const = process_side(left_side)
            right_var, right_const = process_side(right_side)
        except ValueError as e:
            result = jsonify({'error': str(e)})
    
        total_var = left_var - right_var
        total_const = right_const - left_const
    
        if abs(total_var) < 1e-10:  
            if abs(total_const) < 1e-10:
                result = jsonify({'error': 'Equation is always true'})
            else:
                result = jsonify({'error': 'No solution exists'})
    
        solution = total_const / total_var
    
        solution = float_to_fraction_percent(solution, '', False, False)
    
        result = jsonify({
            'values': {
                'letter': letter,
                'solution': solution,
            }
        })
    
    except Exception as e:
        return jsonify({'error': f"Error solving equation: {str(e)}"})
    return result