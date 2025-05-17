import os
from flask import Flask, render_template, request, jsonify
import re
import json
import importlib
import requests
import sys




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
@app.route('/calculators/')
def calculators():
    return render_template('index.html')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def load_cards():
    
    try:
        with open('calculators.json') as f:
            calculators = json.load(f)

        calculator_cards = []

        for calculator in calculators:
            tags = calculator.get('tags', '')
            id = calculator.get('id', '')
            name = calculator.get('name', '')
            description = calculator.get('description', '')
            url = f"<a href=;/calculators/{id}; class=;calculator-card;> "
            url = url.replace(';', '"')
        
            card_html = (
                    f"<div class='calculator-card-wrapper' data-name='{tags}'>"
                    f"{url}"
                    f"    <h3>{name}</h3>"
                    f"    <p>{description}</p>"
                    f"  </a>"
                    f"</div>"
                )
            calculator_cards.append(card_html)

        return jsonify({'cards': calculator_cards})
    except Exception as e:
        return jsonify({'error': str(e)})

#Calculator Code
@app.route('/calculators/solve/<calculator>', methods=['POST'])
def calculator_calculate(calculator):
    try:
        print(f"Received request for calculation from {calculator}")
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        data = request.get_json()
        print(f"Data received: {data}")

        if not re.match(r'^[a-zA-Z0-9_]+$', calculator):
            return jsonify({"error": "Invalid calculator name"}), 400

        solve_function = app.config.get(f'calculator_solve_{calculator}')
        if not solve_function:
            return jsonify({"error": f"Calculator '{calculator}' not found or not loaded"}), 404

        try:
            result = solve_function(data)
            print(f"Result: {result}")
            return result
        except Exception as e:
            print(f"Calculation error: {str(e)}")
            return jsonify({"error": f"Calculation failed: {str(e)}"}), 500
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500
@app.route('/calculators/<calculator>')
def calculator_route(calculator):
    return render_template('calculator.html')
    
@app.route('/loadcalculator<calculatorId>')
def load_calculator(calculatorId):
    print(f"Loading calculator with ID: {calculatorId}")
    try:
        if not re.match(r'^[a-zA-Z0-9_]+$', calculatorId):
            return jsonify({"error": "Invalid calculator name"}), 400

        with open('calculators.json') as f:
            calculators = json.load(f)

        calculator = next((calc for calc in calculators if calc.get('id') == calculatorId), None)
        if calculator is None:
            return jsonify({'error': 'Calculator not found.'}), 404

        module_name = f'python.calculators.{calculatorId}'
        try:
            if module_name in sys.modules:
                calculator_module = importlib.reload(sys.modules[module_name])
            else:
                calculator_module = importlib.import_module(module_name)

            solve_function_name = f'{calculatorId}_solve'
            if not hasattr(calculator_module, solve_function_name):
                return jsonify({"error": f"Calculator '{calculatorId}' has no solve function"}), 404

            app.config[f'calculator_solve_{calculatorId}'] = getattr(calculator_module, solve_function_name)
        except ModuleNotFoundError:
            return jsonify({"error": f"Calculator module '{calculatorId}' not found"}), 404
        except Exception as e:
            print(f"Error importing calculator module: {str(e)}")
            return jsonify({"error": f"Error loading calculator: {str(e)}"}), 500

        title = calculator.get('title', 'Calculator')
        subtitle = calculator.get('subtitle', 'Calculator')

        html = f'''<div class="input-section">
<h2>{title} <small style="color: lightgray;">{subtitle}</small></h2>
<form id="calculatorForm">'''

        selector_input = calculator.get('selectorinput', {})
        if selector_input:
            html += '''<div class="input-group">
<div class="input-label-group">
<label for="operation">Operation:</label>
</div>
<select id="operation" name="operation">'''
            for value, full_text in selector_input.items():
                html += f'<option value="{value}">{full_text}</option>'
            html += '</select></div>'

        numberinput = calculator.get('numberinput', {})
        for input_id, label_text in numberinput.items():
            html += f'''<div class="input-group">
<div class="input-label-group">
<label for="{input_id}">{label_text}</label>
<button type="button" class="clear-single-btn" data-target="{input_id}">
<i data-feather="trash-2"></i>
</button>
</div>
<input type="number" id="{input_id}" step="0.001">
</div>'''

        textinput = calculator.get('textinput', {})
        for input_id, label_text in textinput.items():
            html += f'''<div class="input-group">
<div class="input-label-group">
<label for="{input_id}">{label_text}</label>
<button type="button" class="clear-single-btn" data-target="{input_id}">
<i data-feather="trash-2"></i>
</button>
</div>
<input type="text" id="{input_id}">
</div>'''

        box_count = len(numberinput) + len(textinput)
        clear_box_text = "Clear Box" if box_count == 1 else "Clear Boxes"
        html += f'''<div class="button-group"><button type="Submit" class="generate-btn">Calculate</button><button id="clearButton" class="clear-btn">{clear_box_text}</button></div><div id="error-message" class="error-message"></div></form></div><div class="results-section"><h3>Results:</h3><div id="calculated-values"></div></div></div>'''

        return jsonify({'html': html})
    except Exception as e:
        print(f"Error in load_calculator: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/checkversion')
def version_route():
    github_api_url = "https://api.github.com/repos/LOstDev404/everything-calculator/commits"
    try:
        response = requests.get(github_api_url, headers={
            'Accept': 'application/vnd.github.v3+json',
        })
        if response.status_code == 200:
            commits_data = response.json()
            if commits_data and len(commits_data) > 0:
                latest_commit = commits_data[0]
                commit_name = latest_commit['commit']['message'].split('\n')[0]
                version = f"v{commit_name}"
                return jsonify(version)
            else:
                return jsonify("No commits found")
        else:
            return jsonify(f"API Error: {response.status_code}")
    except Exception as e:
        return jsonify(f"Error: {str(e)}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)