import math
from python.utils import float_to_fraction_percent
from flask import jsonify
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import io
import base64

matplotlib.use('Agg')  

def plot_right_triangle(angle1, angle2, hypotenuse, adjacent, opposite):
    try:
        angle1_str = f"{float(angle1):.3f}"
        angle2_str = f"{float(angle2):.3f}"
        hypotenuse_str = f"{float(hypotenuse):.3f}"
        adjacent_str = f"{float(adjacent):.3f}"
        opposite_str = f"{float(opposite):.3f}"

        fig, ax = plt.subplots(figsize=(6, 6))

        vertices = np.array([[0, 0], [3, 0], [0, 4], [0, 0]])
        ax.plot(vertices[:, 0], vertices[:, 1], 'k-', linewidth=2)

        ax.text(.15, .125, "90°", ha='center', va='center', fontsize=12, fontweight='bold')
        ax.plot([0, 0.3], [0.3, 0.3], 'k-', linewidth=2)
        ax.plot([0.3, 0.3], [0, 0.3], 'k-', linewidth=2)

        if hypotenuse:
            rotation = -np.degrees(np.arctan(4/3))
            ax.text(1.8, 1.8, f"Hypotenuse (C): {hypotenuse_str}", rotation=rotation,
                    ha='center', va='center', fontsize=14, fontweight='bold')

        if adjacent:
            ax.text(1.3, -0.14, f"Adjacent (A): {adjacent_str}",
                    ha='center', va='center', fontsize=14, fontweight='bold')

        if opposite:
            ax.text(-.53, 2, f"Opposite (B):\n{opposite_str}",
                    ha='center', va='center', fontsize=12, fontweight='bold')

        if angle1:
            ax.text(2.8, 0.05, f"Angle 1: {angle1_str}°",
                    ha='right', va='bottom', fontsize=14, fontweight='bold')

        if angle2:
            ax.text(0.04, 2.95, f"Angle 2:\n{angle2_str}°",
                    ha='left', va='top', fontsize=14, fontweight='bold')

        ax.set_aspect('equal')
        ax.axis('off')
        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        plt.close('all')
        return plot_url

    except Exception as e:
        plt.close('all')
        raise e

def trigonometrypythagoreantheorem_solve(data):
    try:
        angle1 = float(data['angle1']) if data.get('angle1') else None
        hypotenuse = float(data['hypotenuse']) if data.get('hypotenuse') else None
        opposite = float(data['opposite']) if data.get('opposite') else None
        adjacent = float(data['adjacent']) if data.get('adjacent') else None

        provided_params = sum(param is not None for param in [angle1, hypotenuse, opposite, adjacent])
        if provided_params != 2:
            result = {'error': 'Please provide exactly two variables to generate a triangle'}
            return jsonify(result)

        if angle1 is not None:
            angle1_rad = math.radians(angle1)
            angle2 = 90 - angle1

            if hypotenuse is not None:
                adjacent = hypotenuse * math.cos(angle1_rad)
                opposite = hypotenuse * math.sin(angle1_rad)

            elif opposite is not None:
                adjacent = opposite / math.tan(angle1_rad)
                hypotenuse = opposite / math.sin(angle1_rad)

            elif adjacent is not None:
                opposite = adjacent * math.tan(angle1_rad)
                hypotenuse = adjacent / math.cos(angle1_rad)

        elif hypotenuse is not None:
            if opposite is not None:
                if hypotenuse < opposite:
                    return jsonify({'error': 'Opposite cannot be greater than hypotenuse'})
                angle1_rad = math.asin(opposite / hypotenuse)
                adjacent = hypotenuse * math.cos(angle1_rad)

            elif adjacent is not None:
                if hypotenuse < adjacent:
                    return jsonify({'error': 'Adjacent cannot be greater than hypotenuse'})
                angle1_rad = math.acos(adjacent / hypotenuse)
                opposite = hypotenuse * math.sin(angle1_rad)

            angle1 = math.degrees(angle1_rad)
            angle2 = 90 - angle1

        elif opposite is not None and adjacent is not None:
            angle1_rad = math.atan(opposite / adjacent)
            hypotenuse = math.sqrt(opposite**2 + adjacent**2)  
            angle1 = math.degrees(angle1_rad)
            angle2 = 90 - angle1

        area = 0.5 * adjacent * opposite
        perimeter = hypotenuse + adjacent + opposite

        plot_url = plot_right_triangle(angle1, angle2, hypotenuse, adjacent, opposite)

        formatted_values = {
            'a1angle1': f"Angle 1: {float_to_fraction_percent(angle1, '°', False, False)}",
            'a2angle2': f"Angle 2: {float_to_fraction_percent(angle2, '°', False, False)}",
            'a3adjacent': f"Adjacent (A): {float_to_fraction_percent(adjacent, '', False, False)}",
            'a4opposite': f"Opposite (B): {float_to_fraction_percent(opposite, '', False, False)}",
            'a5hypotenuse': f"Hypotenuse (C): {float_to_fraction_percent(hypotenuse, '', False, False)}",
            'a6perimeter': f"Perimeter: {float_to_fraction_percent(perimeter, '', False, False)}",
            'a7area': f"Area: {float_to_fraction_percent(area, '', False, False)}",
        }

        result = {
            'plot': plot_url,
            'values': formatted_values
        }

        return jsonify(result)

    except Exception as e:
        result = {'error': str(e)}
        return jsonify(result)