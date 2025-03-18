import os
import matplotlib.pyplot as plt
import matplotlib
from flask import Flask, render_template, request, jsonify
import base64
import io
import math
import re
import numpy as np
from fractions import Fraction


def float_to_fraction_percent(value, suffix, usepercent, purefrac, accuracy=1e-8):
    fraction = Fraction(value).limit_denominator()
    pure_fraction = f"{fraction.numerator}/{fraction.denominator}"

    if fraction.denominator == 1:
        fraction_result = f"{fraction.numerator}/1"
    else:
        whole_number = fraction.numerator // fraction.denominator
        remainder = fraction.numerator % fraction.denominator

        if whole_number == 0:
            fraction_result = f"{remainder}/{fraction.denominator}"
        else:
            fraction_result = f"{whole_number} {remainder}/{fraction.denominator}"

    percentage_result = round(value * 100, 2)

    if usepercent:
        if purefrac:
            return f"{value:.3f}{suffix} | {fraction_result}{suffix} | {percentage_result}{suffix}%", pure_fraction
        else:
            return f"{value:.3f} | {pure_fraction}{suffix} | {percentage_result}%"
    else:
        if purefrac:
            return f"{value:.3f}{suffix} | {fraction_result}{suffix}"
        else:
            return f"{value:.3f}{suffix} | {pure_fraction}{suffix}"

app = Flask(__name__)

def evaluate_expression(expr):
    try:
        expr = expr.strip().lower()
        expr = expr.replace('x', '*')
        expr = expr.replace('^', '**')
        expr = re.sub(r'(\d)(\()', r'\1*\2', expr)
        expr = re.sub(r'(\))(\d)', r'\1*\2', expr)
        expr = re.sub(r'(\))(\()', r'\1*\2', expr)
        expr = re.sub(r'([a-z])(\()', r'\1*\2', expr)
        expr = re.sub(r'(\))([a-z])', r'\1*\2', expr)
        if not re.match(r'^[\d\s\+\-\*\/\(\)\.x\^]*$', expr):
            return None

        result = eval(expr, {"__builtins__": {}})

        if isinstance(result, (int, float)):
            str_result = str(float(result))
            parts = str_result.split('.')
            if len(parts) == 1:
                return f"{parts[0]}.000"
            else:
                decimal_part = (parts[1] + "000")[:3]
                return f"{parts[0]}.{decimal_part}"
        return None
    except:
        return None

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        expression = data.get('expression', '')

        if not any(op in expression for op in ['+', '-', '*', '/', 'x', '(', '^']):
            return jsonify({'result': None})

        result = evaluate_expression(expression)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html") 

@app.route('/sumofinterior')
@app.route('/algebra2step')
def algebra2step():
    return render_template('calculators/algebra2step.html')
@app.route('/algebra2stepcalculate', methods=['POST'])
def algebra2step_result():
    try:    
        data = request.get_json()
        equation = data['algebra2stepequation']
        equation = equation.replace(' ', '').lower()

        if '(' in equation or ')' in equation:
            return jsonify({'error': 'Parentheses are not supported'})

        if '=' not in equation:
            return jsonify({'error': 'Equation must contain an equals sign'})

        if '/' in equation:
            return jsonify({'error': 'Division and fractions are not supported in this calculator'})

        sides = equation.split('=')
        if len(sides) != 2:
            return jsonify({'error': 'You can only use one equal sign.'})
        left_side, right_side = sides

        variables = sorted(set(re.findall(r'[a-z]', equation)))
        if not variables:
            return jsonify({'error': 'No letters/variables in the equation'})
        if len(variables) > 1:
            return jsonify({'error': 'This calculator currently supports only one letter/variable'})
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
            return jsonify({'error': str(e)})

        total_var = left_var - right_var
        total_const = right_const - left_const

        if abs(total_var) < 1e-10:  
            if abs(total_const) < 1e-10:
                return jsonify({'error': 'Equation is always true'})
            else:
                return jsonify({'error': 'No solution exists'})

        solution = total_const / total_var

        solution = float_to_fraction_percent(solution, '', False, False)

        return jsonify({
            'values': {
                'letter': letter,
                'solution': solution,
            }
        })

    except Exception as e:
        return jsonify({'error': f"Error solving equation: {str(e)}"})

@app.route('/patternsequence')
def patternsequence():
    return render_template('calculators/patternsequence.html')
@app.route('/patternsequencecalculate', methods=['POST'])
def patternsequence_calculate():
    try:
        data = request.get_json()
        operation = data['operation']
        firstTerm = float(data['firstTerm'])
        secondTerm = float(data['secondTerm'])
        lastTerm = float(data['lastTerm'])

        if operation == 'add_sub':
            lastTermCalculated = ((lastTerm - 1) * (secondTerm-firstTerm)) + firstTerm
        elif operation == 'mult_div':
            commonRatio = secondTerm / firstTerm

            lastTermCalculated = firstTerm * (commonRatio ** (lastTerm - 1))
        else:
            return jsonify({'error': 'Failed to calculate...'})

        return jsonify({
            'values': {
                'lastTerm': f"{lastTerm:.3f}",
                'lastTermCalculated': f"{lastTermCalculated:.3f}",
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trigonometrypythagoreantheorem')
def trigonometryright():
    return render_template('calculators/trigonometrypythagoreantheorem.html')
#Triangle:
@app.route('/generate_triangle', methods=['POST'])
def generate_triangle():
    def plot_right_triangle(angle1, angle2, hypotenuse, adjacent, opposite):
        matplotlib.use('Agg')
        try:
            angle1 = f"{float(angle1):.3f}"
            angle2 = f"{float(angle2):.3f}"
            hypotenuse = f"{float(hypotenuse):.3f}"
            adjacent = f"{float(adjacent):.3f}"
            opposite = f"{float(opposite):.3f}"
            fig, ax = plt.subplots(figsize=(6, 6))
            vertices = np.array([[0, 0], [3, 0], [0, 4], [0, 0]])
            ax.plot(vertices[:, 0], vertices[:, 1], 'k-', linewidth=2)

            ax.text(.15, .125, "90°", ha='center', va='center', fontsize=12, fontweight='bold')
            ax.plot([0, 0.3], [0.3, 0.3], 'k-', linewidth=2)
            ax.plot([0.3, 0.3], [0, 0.3], 'k-', linewidth=2)
            if hypotenuse:
                rotation = 0 - np.degrees(np.arctan(4/3))
                ax.text(1.8, 1.8, f"Hypotenuse (C): {hypotenuse}", rotation=rotation,
                        ha='center', va='center', fontsize=14, fontweight='bold')

            if adjacent:
                ax.text(1.3, -0.14, f"Adjacent (A): {adjacent}",
                        ha='center', va='center', fontsize=14, fontweight='bold')

            if opposite:
                ax.text(-.53, 2, f"Opposite (B):\n{opposite}",
                        ha='center', va='center', fontsize=12, fontweight='bold')

            if angle1:
                ax.text(2.8, 0.05, f"Angle 1: {angle1}°",
                        ha='right', va='bottom', fontsize=14, fontweight='bold')
            if angle2:
                ax.text(0.04, 2.95, f"Angle 2:\n{angle2}°",
                        ha='left', va='top', fontsize=14, fontweight='bold')

            ax.set_aspect('equal')
            ax.axis('off')
            plt.tight_layout()

            img = io.BytesIO()
            plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()

            plt.close('all')
            img.close()

            return plot_url
        except Exception as e:
            plt.close('all')
            raise e

    try:
        data = request.get_json()
        angle1 = float(data['angle1']) if data['angle1'] else None
        hypotenuse = float(data['hypotenuse']) if data['hypotenuse'] else None
        opposite = float(data['opposite']) if data['opposite'] else None
        adjacent = float(data['adjacent']) if data['adjacent'] else None

        result = {'error': None, 'plot': None}

        if angle1 is not None and hypotenuse is not None:
            angle2 = 90 - angle1
            angle1r = math.radians(angle1)
            adjacent = hypotenuse * math.cos(angle1r)
            opposite = hypotenuse * math.sin(angle1r)

        elif angle1 is not None and opposite is not None:
            angle2 = 90 - angle1
            angle1r = math.radians(angle1)
            adjacent = opposite / math.tan(angle1r)
            hypotenuse = opposite / math.sin(angle1r)

        elif angle1 is not None and adjacent is not None:
            angle2 = 90 - angle1
            angle1r = math.radians(angle1)
            opposite = adjacent * math.tan(angle1r)
            hypotenuse = adjacent / math.cos(angle1r)

        elif opposite is not None and hypotenuse is not None:
            if hypotenuse < opposite:
                return jsonify({'error': 'Opposite cannot be greater than hypotenuse'})
            angle1 = math.asin(opposite / hypotenuse)
            adjacent = hypotenuse * math.cos(angle1)
            angle1 = math.degrees(angle1)
            angle2 = 90 - angle1

        elif opposite is not None and adjacent is not None:
            angle1 = math.atan(opposite / adjacent)
            hypotenuse = adjacent / math.cos(angle1)
            angle1 = math.degrees(angle1)
            angle2 = 90 - angle1

        elif hypotenuse is not None and adjacent is not None:
            if hypotenuse < adjacent:
                return jsonify({'error': 'Adjacent cannot be greater than hypotenuse'})
            angle1 = math.acos(adjacent / hypotenuse)
            opposite = hypotenuse * math.sin(angle1)
            angle1 = math.degrees(angle1)
            angle2 = 90 - angle1
        else:
            return jsonify({'error': 'Please provide two variables to generate a triangle'})
        area = 0.5 * adjacent * opposite
        perimeter = hypotenuse + adjacent + opposite
        plot_url = plot_right_triangle(angle1, angle2, hypotenuse, adjacent, opposite)
        angle1frac = float_to_fraction_percent(angle1, '°', False, False)
        angle2frac = float_to_fraction_percent(angle2, '°', False, False)
        adjacentfrac = float_to_fraction_percent(adjacent, '', False, False)
        oppositefrac = float_to_fraction_percent(opposite, '', False, False)
        hypotenusefrac = float_to_fraction_percent(hypotenuse, '', False, False)
        perimeterfrac = float_to_fraction_percent(perimeter, '', False, False)
        areafrac = float_to_fraction_percent(area, '', False, False)

        return jsonify({
            'plot': plot_url,
            'values': {
                'angle1': f"{angle1:.3f}",
                'angle2': f"{angle2:.3f}",
                'adjacent': f"{adjacent:.3f}",
                'opposite': f"{opposite:.3f}",
                'hypotenuse': f"{hypotenuse:.3f}",
                'perimiter': f"{perimeter:.3f}",
                'area': f"{area:.3f}",
                'angle1frac': f"{angle1frac}",
                'angle2frac': f"{angle2frac}",
                'adjacentfrac': f"{adjacentfrac}",
                'oppositefrac': f"{oppositefrac}",
                'hypotenusefrac': f"{hypotenusefrac}",
                'perimiterfrac': f"{perimeterfrac}",
                'areafrac': f"{areafrac}"
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)})
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)