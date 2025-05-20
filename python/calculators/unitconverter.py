import re
from flask import jsonify

def unitconverter_solve(data):
    try:
        input_text = data.get('inputValue', '').strip()
        if not input_text:
            return jsonify({'error': 'Please enter a measurement with unit'})
        
        parsed = parse_input(input_text)
        if not parsed:
            return jsonify({'error': 'Invalid input format. Please enter a value followed by a unit (e.g., "15 feet", "2.5 kg")'})
        
        value, unit = parsed
        measurement_type, base_unit, base_value = identify_measurement_type(value, unit)
        
        if not measurement_type:
            return jsonify({'error': f'Unknown unit: {unit}'})
            
        conversions = convert_to_all_units(measurement_type, base_value)
        formatted_results = format_results(conversions, measurement_type)
        
        return jsonify({'values': formatted_results})
        
    except Exception as e:
        return jsonify({'error': str(e)})

def parse_input(input_text):
    pattern = r'([-+]?\d*\.?\d+)\s*([a-zA-Z]+\.?|[a-zA-Z]+\s*[a-zA-Z]+)'
    match = re.match(pattern, input_text)
    
    if not match:
        return None
    
    value = float(match.group(1))
    unit = match.group(2).lower().strip()
    
    unit_mapping = {
        'ft': 'feet', 'foot': 'feet', 'feet': 'feet',
        'in': 'inches', 'inch': 'inches', 'inches': 'inches',
        'yd': 'yards', 'yard': 'yards', 'yards': 'yards',
        'mi': 'miles', 'mile': 'miles', 'miles': 'miles',
        'm': 'meters', 'meter': 'meters', 'meters': 'meters',
        'cm': 'centimeters', 'centimeter': 'centimeters', 'centimeters': 'centimeters',
        'mm': 'millimeters', 'millimeter': 'millimeters', 'millimeters': 'millimeters',
        'km': 'kilometers', 'kilometer': 'kilometers', 'kilometers': 'kilometers',
        'g': 'grams', 'gram': 'grams', 'grams': 'grams',
        'kg': 'kilograms', 'kilogram': 'kilograms', 'kilograms': 'kilograms',
        'mg': 'milligrams', 'milligram': 'milligrams', 'milligrams': 'milligrams',
        'lb': 'pounds', 'lbs': 'pounds', 'pound': 'pounds', 'pounds': 'pounds',
        'oz': 'ounces', 'ounce': 'ounces', 'ounces': 'ounces',
        'st': 'stones', 'stone': 'stones', 'stones': 'stones',
        't': 'tonnes', 'ton': 'tonnes', 'metric ton': 'tonnes', 'tonnes': 'tonnes',
        'l': 'liters', 'liter': 'liters', 'liters': 'liters',
        'ml': 'milliliters', 'milliliter': 'milliliters', 'milliliters': 'milliliters',
        'gal': 'gallons', 'gallon': 'gallons', 'gallons': 'gallons',
        'qt': 'quarts', 'quart': 'quarts', 'quarts': 'quarts',
        'pt': 'pints', 'pint': 'pints', 'pints': 'pints',
        'c': 'cups', 'cup': 'cups', 'cups': 'cups',
        'floz': 'fluid ounces', 'fl oz': 'fluid ounces', 'fluid ounce': 'fluid ounces', 'fluid ounces': 'fluid ounces',
        'tbsp': 'tablespoons', 'tablespoon': 'tablespoons', 'tablespoons': 'tablespoons',
        'tsp': 'teaspoons', 'teaspoon': 'teaspoons', 'teaspoons': 'teaspoons'
    }
    
    return value, unit_mapping.get(unit, unit)

def identify_measurement_type(value, unit):
    conversion_factors = {
        'length': {
            'meters': {
                'feet': 0.3048,
                'inches': 0.0254,
                'yards': 0.9144,
                'miles': 1609.34,
                'meters': 1,
                'centimeters': 0.01,
                'millimeters': 0.001,
                'kilometers': 1000
            }
        },
        'mass': {
            'grams': {
                'grams': 1,
                'kilograms': 1000,
                'milligrams': 0.001,
                'pounds': 453.592,
                'ounces': 28.3495,
                'stones': 6350.29,
                'tonnes': 1000000
            }
        },
        'volume': {
            'liters': {
                'liters': 1,
                'milliliters': 0.001,
                'gallons': 3.78541,
                'quarts': 0.946353,
                'pints': 0.473176,
                'cups': 0.236588,
                'fluid ounces': 0.0295735,
                'tablespoons': 0.0147868,
                'teaspoons': 0.00492892
            }
        }
    }
    
    for type_name, type_data in conversion_factors.items():
        for base_unit, units in type_data.items():
            if unit in units:
                return type_name, base_unit, value * units[unit]
    
    return None, None, None

def convert_to_all_units(measurement_type, base_value):
    conversion_factors = {
        'length': {
            'inches': 0.0254,
            'feet': 0.3048,
            'yards': 0.9144,
            'miles': 1609.34,
            'millimeters': 0.001,
            'centimeters': 0.01,
            'meters': 1,
            'kilometers': 1000
        },
        'mass': {
            'ounces': 28.3495,
            'pounds': 453.592,
            'stones': 6350.29,
            'milligrams': 0.001,
            'grams': 1,
            'kilograms': 1000,
            'tonnes': 1000000
        },
        'volume': {
            'teaspoons': 0.00492892,
            'tablespoons': 0.0147868,
            'fluid ounces': 0.0295735,
            'cups': 0.236588,
            'pints': 0.473176,
            'quarts': 0.946353,
            'gallons': 3.78541,
            'milliliters': 0.001,
            'liters': 1
        }
    }
    
    return {unit: base_value / factor for unit, factor in conversion_factors[measurement_type].items()}

def format_results(conversions, measurement_type):
    unit_order = {
        'length': [
            ('inches', 'in'),
            ('feet', 'ft'),
            ('yards', 'yd'),
            ('miles', 'mi'),
            ('millimeters', 'mm'),
            ('centimeters', 'cm'),
            ('meters', 'm'),
            ('kilometers', 'km')
        ],
        'mass': [
            ('ounces', 'oz'),
            ('pounds', 'lb'),
            ('stones', 'st'),
            ('milligrams', 'mg'),
            ('grams', 'g'),
            ('kilograms', 'kg'),
            ('tonnes', 't')
        ],
        'volume': [
            ('teaspoons', 'tsp'),
            ('tablespoons', 'tbsp'),
            ('fluid ounces', 'fl oz'),
            ('cups', 'cup'),
            ('pints', 'pt'),
            ('quarts', 'qt'),
            ('gallons', 'gal'),
            ('milliliters', 'ml'),
            ('liters', 'L')
        ]
    }
    
    formatted_results = {}
    for idx, (unit, abbr) in enumerate(unit_order[measurement_type], 1):
        if unit in conversions:
            value = conversions[unit]
            formatted_results[f"unit{idx}"] = f"{value:.4f} {abbr}"
    
    return formatted_results