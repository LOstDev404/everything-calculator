import os
from flask import Flask, render_template, request, jsonify
import re

#Calculator Imports
from python.calculators.algebra2step import algebra2step_solve
from python.calculators.patternsequence import patternsequence_solve
from python.calculators.circlepolygon import circlepolygon_solve
from python.calculators.trigonometrypythagoreantheorem import trigonometrypythagoreantheorem_solve


app = Flask(__name__)
#Search calculator ------------------------
@app.route('/calculate', methods=['POST'])
def calculate():
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
    try:
        data = request.get_json()
        expression = data.get('expression', '')

        if not any(op in expression for op in ['+', '-', '*', '/', 'x', '(', '^']):
            return jsonify({'result': None})

        result = evaluate_expression(expression)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)})




#Non-Calculator Pages
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")
    
@app.route('/')
def index():
    return render_template('index.html')



#Algebra 2-Step ----------------------------
@app.route('/algebra2step')
def algebra2step():
    return render_template('calculators/algebra2step.html')

@app.route('/algebra2step_calculate', methods=['POST'])
def algebra2step_calculate():
    data = request.get_json()
    result = algebra2step_solve(data)
    return result

#circlepolygon ----------------------------
@app.route('/circlepolygon')
def circlepolygon():
    return render_template('calculators/circlepolygon.html')

@app.route('/circlepolygon_calculate', methods=['POST'])
def circlepolygon_calculate():
    data = request.get_json()
    result = circlepolygon_solve(data)
    return result
    
#Pattern Sequence ----------------------------
@app.route('/patternsequence')
def patternsequence():
    return render_template('calculators/patternsequence.html')

@app.route('/patternsequence_calculate', methods=['POST'])
def patternsequence_calculate():
    data = request.get_json()
    result = patternsequence_solve(data)
    return result

#Trigonometry Pythagorean Theorem------------
@app.route('/trigonometrypythagoreantheorem')
def trigonometryright():
    return render_template('calculators/trigonometrypythagoreantheorem.html')

@app.route('/trigonometrypythagoreantheorem_calculate', methods=['POST'])
def trigonometrypythagoreantheorem_calculate():
    data = request.get_json()
    result = trigonometrypythagoreantheorem_solve(data)
    return result

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)