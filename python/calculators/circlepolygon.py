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

            sumOfInt = (sides - 2) * 180
            shape = shape_name(sides)
            return jsonify({
                'values': {
                    'a1shape': f"Shape: {shape}",
                    'a2area': f"Area: {area:.3f}",
                    'a3perimeterc': f"Perimeter: {perimeter:.3f}",
                    'a4radiusDiameterInterior': f"Sum of Interior Angles: {sumOfInt}"
                }
            })
        
    
        elif radiusSides != '' and diameterLength == '':
            radius = float(radiusSides)
            diameter = radius * 2
            perimeter = 2 * math.pi * radius
            perimeterFrac = 2 * radius
    
            area = math.pi * radius**2
            areaFrac = radius**2
            shape = "Circle"
            return jsonify({
                'values': {
                    'a1shape': f"Shape: {shape}",
                    'a2area': f"Area: {areaFrac:.3f}π²",
                    'a3perimeter': f"Circumference: {perimeterFrac:.3f}π²",
                    'a4radiusDiameterInterior': f"Diameter: {diameter:.3f}"
                }
            })
           
    
        elif diameterLength != '' and  radiusSides == '':
            diameter = float(diameterLength)
            radius = diameter / 2
            perimeter = 2 * math.pi * radius
            perimeterFrac = 2 * radius
    
            area = math.pi * radius**2
            areaFrac = radius**2
            shape = "Circle"
            return jsonify({
                'values': {
                    'a1shape': f"Shape: {shape}",
                    'a2area': f"Area: {areaFrac:.3f}π²",
                    'a3perimeter': f"Circumference: {perimeterFrac:.3f}π²",
                    'a4radiusDiameterInterior': f"Radius: {radius:.3f}"
                }
            })
            
    
        else:
            return jsonify({'error': 'Please fill at least one of the input fields'})
            
            
    except Exception as e:
        result = jsonify({'error': str(e)})
        return result