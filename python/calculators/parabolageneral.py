from flask import jsonify
from fractions import Fraction
from python.utils import float_to_fraction_percent
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import io
import base64

matplotlib.use('Agg')

def plot_parabola(a, b, c, xv, yv, axis):
    try:
        L_base = 10
        key_extents = [abs(xv), abs(axis), abs(yv), abs(c)]
        max_abs_key = max(key_extents + [L_base])
        if max_abs_key > L_base:
            L = int(np.ceil(max_abs_key)) + 1
        else:
            L = L_base

        x = np.linspace(-L, L, 600)
        y = a * x**2 + b * x + c

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.plot(x, y, 'b-', linewidth=2)

        ax.plot([xv], [yv], 'ro')
        ax.annotate(f"Vertex ({xv:.3f}, {yv:.3f})", xy=(xv, yv), xytext=(xv + 0.15*L, yv),
                    arrowprops=dict(arrowstyle='->', color='red'), color='red', fontsize=10)
        ax.axvline(x=axis, color='gray', linestyle='--', linewidth=1.5)
        y_int = c
        ax.plot([0], [y_int], 'go')
        ax.annotate(f"Y-Intercept (0, {y_int:.3f})", xy=(0, y_int), xytext=(0.1*L, y_int + 0.1*L),
                    arrowprops=dict(arrowstyle='->', color='green'), color='green', fontsize=10)
        ax.set_xlim(-L, L)
        ax.set_ylim(-L, L)
        ax.set_aspect('equal', adjustable='box')
        
        ax.axvline(0, color='black', linewidth=2)
        ax.axhline(0, color='black', linewidth=2)

        ax.xaxis.tick_top()
        ax.yaxis.tick_left()
        step = 1 if L <= 20 else int(np.ceil(L / 10))
        ax.set_xticks(np.arange(-L, L + 1, step))
        ax.set_yticks(np.arange(-L, L + 1, step))
        ax.tick_params(axis='both', which='major', labelsize=9)

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight', dpi=110)
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close('all')
        return plot_url
    except Exception as e:
        plt.close('all')
        raise e

def parabolageneral_solve(data):
    try:
        a_raw = data.get('aCoeff')
        b_raw = data.get('bCoeff')
        c_raw = data.get('cCoeff')

        if a_raw is None or str(a_raw).strip() == '':
            a = 1.0
        else:
            try:
                a = float(a_raw)
            except (TypeError, ValueError):
                return jsonify({'error': 'Invalid A coefficient; please enter a number or leave blank'})

        if b_raw is None or str(b_raw).strip() == '':
            b = 0.0
        else:
            try:
                b = float(b_raw)
            except (TypeError, ValueError):
                return jsonify({'error': 'Invalid B coefficient; please enter a number or leave blank'})

        if c_raw is None or str(c_raw).strip() == '':
            return jsonify({'error': 'C coefficient is required'})
        else:
            try:
                c = float(c_raw)
            except (TypeError, ValueError):
                return jsonify({'error': 'Invalid C coefficient; please enter a number'})

        opens = 'Opens Up' if a > 0 else 'Opens Down' if a < 0 else 'Not a parabola (a=0)'

        if a == 0:
            return jsonify({'error': 'Coefficient A must be non-zero for a parabola'})

        xv = -b / (2 * a)
        yv = a * (xv ** 2) + b * xv + c

        axis = xv

        y_intercept = c

        min_or_max = 'Minimum' if a > 0 else 'Maximum'
        minmax_value = yv

        def fmt_decimal(val):
            try:
                return f"{float(val):.3f}"
            except:
                return str(val)

        def fmt_frac(val):
            try:
                return float_to_fraction_percent(val)
            except:
                return str(val)

        vertex_pair_decimal = f"({fmt_decimal(xv)}, {fmt_decimal(yv)})"
        vertex_pair_frac = f"({fmt_frac(xv)}, {fmt_frac(yv)})"

        values = {
            'ayIntercept': f"Y-Intercept: {fmt_decimal(y_intercept)}",
            #'yInterceptFrac': f"Y-Intercept: {fmt_frac(y_intercept)}",
            'cvertex': f"Vertex: {vertex_pair_decimal}",
            #'vertexFrac': f"Vertex: {vertex_pair_frac}",
            'baxisOfSymmetry': f"Axis of Symmetry: x = {fmt_decimal(axis)}",
            #'axisOfSymmetryFrac': f"Axis of Symmetry: x = {fmt_frac(axis)}",
            'eopens': f"{opens}",
            'dminMax': f"{min_or_max} ({fmt_decimal(minmax_value)})",
            #'minMaxFrac': f"{min_or_max} ({fmt_frac(minmax_value)})",
        }

        plot_url = plot_parabola(a, b, c, xv, yv, axis)

        return jsonify({'plot': plot_url, 'values': values})
    except Exception as e:
        return jsonify({'error': f'Error solving parabola: {str(e)}'})