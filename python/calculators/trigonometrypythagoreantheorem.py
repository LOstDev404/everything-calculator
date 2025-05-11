import math
from python.utils import float_to_fraction_percent
from flask import jsonify
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import io
import base64

def trigonometrypythagoreantheorem_solve(data):
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
                result = jsonify({'error': 'Opposite cannot be greater than hypotenuse'})
                return result
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
                result = jsonify({'error': 'Adjacent cannot be greater than hypotenuse'})
                return result
            angle1 = math.acos(adjacent / hypotenuse)
            opposite = hypotenuse * math.sin(angle1)
            angle1 = math.degrees(angle1)
            angle2 = 90 - angle1
        else:
            result = jsonify({'error': 'Please provide two variables to generate a triangle'})
            return result
        area = 0.5 * adjacent * opposite
        perimeter = hypotenuse + adjacent + opposite
        plot_url = plot_right_triangle(angle1, angle2, hypotenuse, adjacent, opposite)
        angle1Frac = float_to_fraction_percent(angle1, '°', False, False)
        angle2Frac = float_to_fraction_percent(angle2, '°', False, False)
        adjacentFrac = float_to_fraction_percent(adjacent, '', False, False)
        oppositeFrac = float_to_fraction_percent(opposite, '', False, False)
        hypotenuseFrac = float_to_fraction_percent(hypotenuse, '', False, False)
        perimeterFrac = float_to_fraction_percent(perimeter, '', False, False)
        areaFrac = float_to_fraction_percent(area, '', False, False)

        result = jsonify({
            'plot': plot_url,
            'values': {
                'angle1': f"Angle 1: {angle1Frac}",
                'angle2': f"Angle 2: {angle2Frac}",
                'adjacent': f"Adjacent (A): {adjacentFrac}",
                'opposite': f"Opposite (B): {oppositeFrac}",
                'hypotenuse': f"Hypotenuse (C): {hypotenuseFrac}",
                'perimeter': f"Perimeter: {perimeterFrac}",
                'area': f"Area: {areaFrac}",
        }})
        return result

    except Exception as e:
        result = jsonify({'error': str(e)})
        return result