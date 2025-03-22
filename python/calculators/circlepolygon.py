from python.utils import float_to_fraction_percent
from python.utils import shape_name
from flask import jsonify
import math


def circlepolygon_solve(data):
    diameterLength = data['diameterLength']
    radiusSides = data['radiusSides']
    
    try:    
        if radiusSides != '' and diameterLength != '':
            length = float(diameterLength)
            sides = float(radiusSides)
            if sides < 3:
                result = jsonify({'error': 'The amount of sides must be more than 2'})
                return result
    
            perimeter = sides * length
            area = (sides * length**2) / (4 * math.tan(math.pi / sides))
    
            areaFrac = float_to_fraction_percent(area, '²', False, True)
            perimeterFrac = float_to_fraction_percent(perimeter, '²', False, True)
            sumOfInt = (sides - 2) * 180
            shape = shape_name(sides)
            result = jsonify({
                'values': {
                    'shape': f"{shape}",
                    'areaFrac': f"{areaFrac}",
                    'perimeterFrac': f"Perimeter: {perimeterFrac}",
                    'radiusDiameterInterior': f"Sum of Interior Angles: {sumOfInt}"
                }
            })
            return result
    
        elif radiusSides != '' and diameterLength == '':
            radius = float(radiusSides)
            diameter = radius * 2
            perimeter = 2 * math.pi * radius
            perimeterFrac = 2 * radius
    
            area = math.pi * radius**2
            areaFrac = radius**2
            shape = "Circle"
            result = jsonify({
                'values': {
                    'shape': f"{shape}",
                    'areaFrac': f"{area:.3f}² | {areaFrac:.3f}π²",
                    'perimeterFrac': f"Circumference: {perimeter:.3f}² | {perimeterFrac:.3f}π²",
                    'radiusDiameterInterior': f"Diameter: {diameter}"
                }
            })
            return result
    
        elif diameterLength != '' and  radiusSides == '':
            diameter = float(diameterLength)
            radius = diameter / 2
            perimeter = 2 * math.pi * radius
            perimeterFrac = 2 * radius
    
            area = math.pi * radius**2
            areaFrac = radius**2
            shape = "Circle"
            result = jsonify({
                'values': {
                    'shape': f"{shape}",
                    'areaFrac': f"{area:.3f}² | {areaFrac:.3f}π²",
                    'perimeterFrac': f"Circumference: {perimeter:.3f}² | {perimeterFrac:.3f}π²",
                    'radiusDiameterInterior': f"Radius: {radius}"
                }
            })
            return result
    
        else:
            result = jsonify({'error': 'Please fill at least one of the input fields'})
            return result
            
    except Exception as e:
        result = jsonify({'error': str(e)})
        return result