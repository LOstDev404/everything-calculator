import os
from flask import Flask, render_template, request, jsonify
import re
import json
import importlib
import requests
import sys
import matplotlib 
import numpy as np
import sympy
import math
import matplotlib.pyplot as plt
import io
import base64
from sympy import Eq, symbols, solve, sympify
from functools import lru_cache


app = Flask(__name__)

# Cache calculator.json ------------------------
@lru_cache(maxsize=1)
def get_calculators_config():
    with open('calculators.json') as f:
        return json.load(f)

# Search calculator ------------------------
@app.route('/calculate', methods=['POST'])
def calculate():
    def evaluate_expression(expr):
        try:
            expr = expr.strip().lower()
            replacements = [
                ('x', '*'),
                ('^', '**'),
                (r'(\d)(\()', r'\1*\2'),
                (r'(\))(\d)', r'\1*\2'),
                (r'(\))(\()', r'\1*\2'),
                (r'([a-z])(\()', r'\1*\2'),
                (r'(\))([a-z])', r'\1*\2')
            ]
            for old, new in replacements:
                expr = re.sub(old, new, expr) if '(' in old else expr.replace(old, new)
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

# Non-Calculator Pages
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
        calculators = get_calculators_config()
        calculator_cards = []

        for calculator in calculators:
            tags = calculator.get('tags', '')
            id = calculator.get('id', '')
            name = calculator.get('name', '')
            description = calculator.get('description', '')
            url = f'<a href="/calculators/{id}" class="calculator-card">'

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

# Get calculator solve function
def get_calculator_solve_function(calculator_id):
    if not re.match(r'^[a-zA-Z0-9_]+$', calculator_id):
        raise ValueError("Invalid calculator name")

    solve_function_key = f'calculator_solve_{calculator_id}'
    solve_function = app.config.get(solve_function_key)

    if not solve_function:
        try:
            module_name = f'python.calculators.{calculator_id}'

            if module_name in sys.modules:
                if app.config.get('ENV') == 'development':
                    importlib.reload(sys.modules[module_name])
                calculator_module = sys.modules[module_name]
            else:
                calculator_module = importlib.import_module(module_name)

            solve_function_name = f'{calculator_id}_solve'

            if hasattr(calculator_module, solve_function_name):
                solve_function = getattr(calculator_module, solve_function_name)
                app.config[solve_function_key] = solve_function
            else:
                raise ValueError(f"Calculator '{calculator_id}' has no solve function")
        except Exception as e:
            raise ValueError(f"Calculator '{calculator_id}' not found or not loaded: {str(e)}")

    return solve_function

# Calculator Solve Code
@app.route('/calculators/solve/<calculator>', methods=['POST'])
def calculator_calculate(calculator):
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()

        try:
            solve_function = get_calculator_solve_function(calculator)
            result = solve_function(data)
            return result
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": f"Calculation failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# Load Calculator Page
@app.route('/calculators/<calculator>')
def calculator_route(calculator):
    return render_template('calculator.html')

# Load Calculator Form
@app.route('/loadcalculator<calculatorId>')
def load_calculator(calculatorId):
    try:
        calculators_config = get_calculators_config()
        calculator = next((calc for calc in calculators_config if calc.get('id') == calculatorId), None)

        if calculator is None:
            return jsonify({'error': 'Calculator not found.'}), 404

        try:
            get_calculator_solve_function(calculatorId)
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": f"Error loading calculator module: {str(e)}"}), 500

        title = calculator.get('title', 'Calculator')
        subtitle = calculator.get('subtitle', '')

        html_parts = ['<div class="input-section">\n']
        html_parts.append(f'<h2>{title} <small style="color: lightgray;">{subtitle}</small></h2>\n')
        html_parts.append('<form id="calculatorForm">\n')

        selector_input = calculator.get('selectorinput', {})
        if selector_input:
            html_parts.append('    <div class="input-group">\n')
            html_parts.append('        <div class="input-label-group">\n')
            html_parts.append('            <label for="operation">Operation:</label>\n')
            html_parts.append('        </div>\n')
            html_parts.append('        <select id="operation" name="operation">\n')
            for value, full_text in selector_input.items():
                html_parts.append(f'            <option value="{value}">{full_text}</option>\n')
            html_parts.append('        </select>\n')
            html_parts.append('    </div>\n')

        numberinput = calculator.get('numberinput', {})
        for input_id, label_text in numberinput.items():
            html_parts.append('    <div class="input-group">\n')
            html_parts.append('        <div class="input-label-group">\n')
            html_parts.append(f'            <label for="{input_id}">{label_text}</label>\n')
            html_parts.append(f'            <button type="button" class="clear-single-btn" data-target="{input_id}">\n')
            html_parts.append('                <i data-feather="trash-2"></i>\n')
            html_parts.append('            </button>\n')
            html_parts.append('        </div>\n')
            html_parts.append(f'        <input type="number" id="{input_id}" step="0.001">\n')
            html_parts.append('    </div>\n')

        textinput = calculator.get('textinput', {})
        for input_id, label_text in textinput.items():
            html_parts.append('    <div class="input-group">\n')
            html_parts.append('        <div class="input-label-group">\n')
            html_parts.append(f'            <label for="{input_id}">{label_text}</label>\n')
            html_parts.append(f'            <button type="button" class="clear-single-btn" data-target="{input_id}">\n')
            html_parts.append('                <i data-feather="trash-2"></i>\n')
            html_parts.append('            </button>\n')
            html_parts.append('        </div>\n')
            html_parts.append(f'        <input type="text" id="{input_id}">\n')
            html_parts.append('    </div>\n')

        box_count = len(numberinput) + len(textinput)
        clear_box_text = "Clear Box" if box_count == 1 else "Clear Boxes"

        button_section = (
            f'<div class="button-group">'
            f'<button type="Submit" class="generate-btn">Calculate</button>'
            f'<button id="clearButton" class="clear-btn">{clear_box_text}</button>'
            f'</div>'
            f'<div id="error-message" class="error-message"></div>'
        )
        html_parts.append(button_section)

        results_section = (
            '</form></div>'
            '<div class="results-section">'
            '<h2>Results:</h2>'
            '<div id="calculated-values"></div>'
            '</div></div></div>'
        )
        html_parts.append(results_section)

        return jsonify({'html': ''.join(html_parts)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Version Check for Footer
@app.route('/checkversion')
def version_route():
    github_api_url = "https://api.github.com/repos/LOstDev404/everything-calculator/commits"
    try:
        response = requests.get(github_api_url, headers={
            'Accept': 'application/vnd.github.v3+json',
        })

        if response.status_code != 200:
            return jsonify(f"API Error: {response.status_code}")

        commits_data = response.json()
        if not commits_data:
            return jsonify("No commits found")

        latest_commit = commits_data[0]
        commit_name = latest_commit['commit']['message'].split('\n')[0]
        version = f"v{commit_name}"
        return jsonify(version)

    except Exception as e:
        return jsonify(f"Error: {str(e)}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)