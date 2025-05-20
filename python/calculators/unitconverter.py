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
            
        conversions = convert_to_all_units(measurement_type, base_unit, base_value)
        
        formatted_results = format_results(conversions, measurement_type)
        
        return jsonify({
            'values': formatted_results
        })
        
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
    
    for key, normalized_unit in unit_mapping.items():
        if unit == key:
            unit = normalized_unit
            break
    
    return value, unit

def identify_measurement_type(value, unit):
    conversion_factors = {
        'feet': ('length', 'meters', lambda x: x * 0.3048),
        'inches': ('length', 'meters', lambda x: x * 0.0254),
        'yards': ('length', 'meters', lambda x: x * 0.9144),
        'miles': ('length', 'meters', lambda x: x * 1609.34),
        'meters': ('length', 'meters', lambda x: x),
        'centimeters': ('length', 'meters', lambda x: x * 0.01),
        'millimeters': ('length', 'meters', lambda x: x * 0.001),
        'kilometers': ('length', 'meters', lambda x: x * 1000),
        
        'grams': ('mass', 'grams', lambda x: x),
        'kilograms': ('mass', 'grams', lambda x: x * 1000),
        'milligrams': ('mass', 'grams', lambda x: x * 0.001),
        'pounds': ('mass', 'grams', lambda x: x * 453.592),
        'ounces': ('mass', 'grams', lambda x: x * 28.3495),
        'stones': ('mass', 'grams', lambda x: x * 6350.29),
        'tonnes': ('mass', 'grams', lambda x: x * 1000000),
        
        'liters': ('volume', 'liters', lambda x: x),
        'milliliters': ('volume', 'liters', lambda x: x * 0.001),
        'gallons': ('volume', 'liters', lambda x: x * 3.78541),
        'quarts': ('volume', 'liters', lambda x: x * 0.946353),
        'pints': ('volume', 'liters', lambda x: x * 0.473176),
        'cups': ('volume', 'liters', lambda x: x * 0.236588),
        'fluid ounces': ('volume', 'liters', lambda x: x * 0.0295735),
        'tablespoons': ('volume', 'liters', lambda x: x * 0.0147868),
        'teaspoons': ('volume', 'liters', lambda x: x * 0.00492892)
    }
    
    if unit not in conversion_factors:
        return None, None, None
        
    measurement_type, base_unit, conversion_func = conversion_factors[unit]
    base_value = conversion_func(value)
    
    return measurement_type, base_unit, base_value

def convert_to_all_units(measurement_type, base_unit, base_value):
    conversions = {}
    
    if measurement_type == 'length':
        conversions['inches'] = base_value / 0.0254
        conversions['feet'] = base_value / 0.3048
        conversions['yards'] = base_value / 0.9144
        conversions['miles'] = base_value / 1609.34
        conversions['millimeters'] = base_value * 1000
        conversions['centimeters'] = base_value * 100
        conversions['meters'] = base_value
        conversions['kilometers'] = base_value / 1000
        
    elif measurement_type == 'mass':
        conversions['ounces'] = base_value / 28.3495
        conversions['pounds'] = base_value / 453.592
        conversions['stones'] = base_value / 6350.29
        conversions['milligrams'] = base_value * 1000
        conversions['grams'] = base_value
        conversions['kilograms'] = base_value / 1000
        conversions['tonnes'] = base_value / 1000000
        
    elif measurement_type == 'volume':
        conversions['teaspoons'] = base_value / 0.00492892
        conversions['tablespoons'] = base_value / 0.0147868
        conversions['fluid ounces'] = base_value / 0.0295735
        conversions['cups'] = base_value / 0.236588
        conversions['pints'] = base_value / 0.473176
        conversions['quarts'] = base_value / 0.946353
        conversions['gallons'] = base_value / 3.78541
        conversions['milliliters'] = base_value * 1000
        conversions['liters'] = base_value
        
    return conversions

def format_results(conversions, measurement_type):
    formatted_results = {}
    
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
    
    count = 1
    for unit, abbr in unit_order[measurement_type]:
        if unit in conversions:
            value = conversions[unit]
            decimal = f"{value:.4f}"
            
            unit_key = f"unit{count}"
            formatted_results[unit_key] = f"{decimal} {abbr}"
            
            count += 1
    
    return formatted_results