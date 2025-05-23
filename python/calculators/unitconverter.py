import re
from flask import jsonify
from python.utils import get_unit_mappings

def unitconverter_solve(data):
    try:
        input_text = data.get('inputValue', '').strip()
        if not input_text:
            return jsonify({'error': 'Please enter a measurement with unit'})

        target_unit = None
        if ' to ' in input_text.lower():
            parts = input_text.lower().split(' to ')
            if len(parts) == 2:
                input_text = parts[0].strip()
                target_unit = parts[1].strip()

        parsed = parse_input(input_text)
        if not parsed:
            return jsonify({'error': 'Invalid input format. Please enter a value followed by a unit (e.g., "15 feet", "2.5 kg")'})

        value, unit = parsed
        measurement_type, base_unit, base_value = identify_measurement_type(value, unit)

        if not measurement_type:
            return jsonify({'error': f'Unknown unit: {unit}'})

        conversions = convert_to_all_units(measurement_type, base_value)
        formatted_results = format_results(conversions, measurement_type, target_unit)

        return jsonify({'values': formatted_results})

    except Exception as e:
        return jsonify({'error': str(e)})

def parse_input(input_text):
    pattern = r'([-+]?\d*\.?\d+)\s*([a-zA-Z]+\.?|[a-zA-Z]+\s*[a-zA-Z]+|°[a-zA-Z]|[a-zA-Z]+\s+[a-zA-Z]+)'
    match = re.match(pattern, input_text)

    if not match:
        return None

    value = float(match.group(1))
    unit = match.group(2).lower().strip()

    unit_mapping = get_unit_mappings()
    
    if 'cubed' in unit:
        unit = unit.replace('cubed', '').strip()
        if unit in unit_mapping:
            base_unit = unit_mapping[unit]
            if base_unit in ['feet', 'inches', 'yards', 'meters', 'centimeters', 'millimeters', 'kilometers', 'decimeters', 'dekameters', 'hectometers']:
                unit = f'cubic {base_unit}'
    
    return value, unit_mapping.get(unit, unit)

def identify_measurement_type(value, unit):
    conversion_factors = {
        'length': {
            'meters': {
                'feet': 0.3048, 'inches': 0.0254, 'yards': 0.9144, 'miles': 1609.34,
                'meters': 1, 'centimeters': 0.01, 'millimeters': 0.001, 'kilometers': 1000,
                'decimeters': 0.1, 'dekameters': 10, 'hectometers': 100,
                'micrometers': 0.000001, 'nanometers': 0.000000001, 'picometers': 0.000000000001,
                'astronomical units': 149597870700, 'light years': 9460730472580800
            }
        },
        'mass': {
            'grams': {
                'grams': 1, 'kilograms': 1000, 'milligrams': 0.001, 'micrograms': 0.000001,
                'nanograms': 0.000000001, 'picograms': 0.000000000001, 'decigrams': 0.1,
                'dekagrams': 10, 'hectograms': 100, 'pounds': 453.592, 'ounces': 28.3495,
                'stones': 6350.29, 'tonnes': 1000000, 'carats': 0.2, 'grains': 0.06479891,
                'pennyweights': 1.55517384
            }
        },
        'volume': {
            'liters': {
                'liters': 1, 'milliliters': 0.001, 'centiliters': 0.01, 'deciliters': 0.1,
                'dekaliters': 10, 'hectoliters': 100, 'kiloliters': 1000,
                'microliters': 0.000001, 'nanoliters': 0.000000001, 'picoliters': 0.000000000001,
                'gallons': 3.78541, 'quarts': 0.946353, 'pints': 0.473176, 'cups': 0.236588,
                'fluid ounces': 0.0295735, 'tablespoons': 0.0147868, 'teaspoons': 0.00492892,
                'barrels': 119.24, 'cubic feet': 28.3168, 'cubic inches': 0.0163871, 'cubic yards': 764.555,
                'cubic meters': 1000, 'cubic centimeters': 0.001, 'cubic millimeters': 0.000001,
                'cubic kilometers': 1000000000000, 'cubic decimeters': 1, 'cubic dekameters': 1000000,
                'cubic hectometers': 1000000000
            }
        },
        'data': {
            'bits': {
                'bits': 1, 'kilobits': 1000, 'megabits': 1000000, 'gigabits': 1000000000,
                'terabits': 1000000000000, 'petabits': 1000000000000000,
                'bytes': 8, 'kibibytes': 8192, 'mebibytes': 8388608, 'gibibytes': 8589934592,
                'tebibytes': 8796093022208, 'pebibytes': 9007199254740992,
                'kilobytes decimal': 8000, 'megabytes decimal': 8000000, 'gigabytes decimal': 8000000000,
                'terabytes decimal': 8000000000000, 'petabytes decimal': 8000000000000000
            }
        },
        'temperature': {
            'celsius': {
                'celsius': 1, 'fahrenheit': 1, 'kelvin': 1, 'rankine': 1
            }
        }
    }

    for type_name, type_data in conversion_factors.items():
        for base_unit, units in type_data.items():
            if unit in units:
                if type_name == 'temperature':
                    base_value = convert_temperature_to_celsius(value, unit)
                    return type_name, 'celsius', base_value
                else:
                    return type_name, base_unit, value * units[unit]

    return None, None, None

def convert_temperature_to_celsius(value, unit):
    if unit == 'fahrenheit':
        return (value - 32) * 5/9
    elif unit == 'kelvin':
        return value - 273.15
    elif unit == 'rankine':
        return (value - 491.67) * 5/9
    else:
        return value

def convert_celsius_to_unit(celsius_value, unit):
    if unit == 'fahrenheit':
        return celsius_value * 9/5 + 32
    elif unit == 'kelvin':
        return celsius_value + 273.15
    elif unit == 'rankine':
        return (celsius_value + 273.15) * 9/5
    else:
        return celsius_value

def convert_to_all_units(measurement_type, base_value):
    conversion_factors = {
        'length': {
            'inches': 0.0254, 'feet': 0.3048, 'yards': 0.9144, 'miles': 1609.34,
            'millimeters': 0.001, 'centimeters': 0.01, 'decimeters': 0.1, 'meters': 1,
            'dekameters': 10, 'hectometers': 100, 'kilometers': 1000,
            'micrometers': 0.000001, 'nanometers': 0.000000001, 'picometers': 0.000000000001,
            'astronomical units': 149597870700, 'light years': 9460730472580800
        },
        'mass': {
            'ounces': 28.3495, 'pounds': 453.592, 'stones': 6350.29,
            'picograms': 0.000000000001, 'nanograms': 0.000000001, 'micrograms': 0.000001,
            'milligrams': 0.001, 'decigrams': 0.1, 'grams': 1, 'dekagrams': 10,
            'hectograms': 100, 'kilograms': 1000, 'tonnes': 1000000,
            'carats': 0.2, 'grains': 0.06479891, 'pennyweights': 1.55517384
        },
        'volume': {
            'teaspoons': 0.00492892, 'tablespoons': 0.0147868, 'fluid ounces': 0.0295735,
            'cups': 0.236588, 'pints': 0.473176, 'quarts': 0.946353, 'gallons': 3.78541,
            'picoliters': 0.000000000001, 'nanoliters': 0.000000001, 'microliters': 0.000001,
            'milliliters': 0.001, 'centiliters': 0.01, 'deciliters': 0.1, 'liters': 1,
            'dekaliters': 10, 'hectoliters': 100, 'kiloliters': 1000, 'barrels': 119.24,
            'cubic inches': 0.0163871, 'cubic feet': 28.3168, 'cubic yards': 764.555,
            'cubic millimeters': 0.000001, 'cubic centimeters': 0.001, 'cubic decimeters': 1,
            'cubic meters': 1000, 'cubic dekameters': 1000000, 'cubic hectometers': 1000000000,
            'cubic kilometers': 1000000000000
        },
        'data': {
            'bits': 1, 'kilobits': 1000, 'megabits': 1000000, 'gigabits': 1000000000,
            'terabits': 1000000000000, 'petabits': 1000000000000000,
            'bytes': 8, 'kibibytes': 8192, 'mebibytes': 8388608, 'gibibytes': 8589934592,
            'tebibytes': 8796093022208, 'pebibytes': 9007199254740992,
            'kilobytes decimal': 8000, 'megabytes decimal': 8000000, 'gigabytes decimal': 8000000000,
            'terabytes decimal': 8000000000000, 'petabytes decimal': 8000000000000000
        },
        'temperature': {
            'celsius': 1, 'fahrenheit': 1, 'kelvin': 1, 'rankine': 1
        }
    }

    if measurement_type == 'temperature':
        return {unit: convert_celsius_to_unit(base_value, unit) for unit in conversion_factors[measurement_type]}
    else:
        return {unit: base_value / factor for unit, factor in conversion_factors[measurement_type].items()}

def get_unit_aliases():
    unit_mappings = get_unit_mappings()
    aliases = {}
    
    for aliases_list, canonical in unit_mappings.items():
        if canonical not in aliases:
            aliases[canonical] = []
        aliases[canonical].append(aliases_list)
    
    return aliases

def format_results(conversions, measurement_type, target_unit=None):
    unit_order = {
        'length': [
            ('inches', 'in'), ('feet', 'ft'), ('yards', 'yd'), ('miles', 'mi'),
            ('picometers', 'pm'), ('nanometers', 'nm'), ('micrometers', 'μm'),
            ('millimeters', 'mm'), ('centimeters', 'cm'), ('decimeters', 'dm'),
            ('meters', 'm'), ('dekameters', 'dam'), ('hectometers', 'hm'),
            ('kilometers', 'km'), ('astronomical units', 'AU'), ('light years', 'ly')
        ],
        'mass': [
            ('ounces', 'oz'), ('pounds', 'lb'), ('stones', 'st'),
            ('picograms', 'pg'), ('nanograms', 'ng'), ('micrograms', 'μg'),
            ('milligrams', 'mg'), ('decigrams', 'dg'), ('grams', 'g'),
            ('dekagrams', 'dag'), ('hectograms', 'hg'), ('kilograms', 'kg'),
            ('tonnes', 't'), ('carats', 'ct'), ('grains', 'gr'), ('pennyweights', 'dwt')
        ],
        'volume': [
            ('teaspoons', 'tsp'), ('tablespoons', 'tbsp'), ('fluid ounces', 'fl oz'),
            ('cups', 'cup'), ('pints', 'pt'), ('quarts', 'qt'), ('gallons', 'gal'),
            ('picoliters', 'pL'), ('nanoliters', 'nL'), ('microliters', 'μL'),
            ('milliliters', 'mL'), ('centiliters', 'cL'), ('deciliters', 'dL'),
            ('liters', 'L'), ('dekaliters', 'daL'), ('hectoliters', 'hL'),
            ('kiloliters', 'kL'), ('barrels', 'bbl'), ('cubic inches', 'in³'),
            ('cubic feet', 'ft³'), ('cubic yards', 'yd³'), ('cubic millimeters', 'mm³'),
            ('cubic centimeters', 'cm³'), ('cubic decimeters', 'dm³'),
            ('cubic meters', 'm³'), ('cubic dekameters', 'dam³'),
            ('cubic hectometers', 'hm³'), ('cubic kilometers', 'km³')
        ],
        'data': [
            ('bits', 'b'), ('kilobits', 'Kb'), ('megabits', 'Mb'),
            ('gigabits', 'Gb'), ('terabits', 'Tb'), ('petabits', 'Pb'),
            ('bytes', 'B'), ('kibibytes', 'KiB'), ('mebibytes', 'MiB'),
            ('gibibytes', 'GiB'), ('tebibytes', 'TiB'), ('pebibytes', 'PiB'),
            ('kilobytes decimal', 'KB'), ('megabytes decimal', 'MB'),
            ('gigabytes decimal', 'GB'), ('terabytes decimal', 'TB'),
            ('petabytes decimal', 'PB')
        ],
        'temperature': [
            ('celsius', '°C'), ('fahrenheit', '°F'), ('kelvin', 'K'), ('rankine', '°R')
        ]
    }

    formatted_results = {}
    target_found = False
    aliases = get_unit_aliases()

    for idx, (unit, abbr) in enumerate(unit_order[measurement_type], 1):
        if unit in conversions:
            value = conversions[unit]
            
            unit_alias_list = aliases.get(unit, [unit])
            unit_alias_string = ' '.join(unit_alias_list)
            
            if target_unit and (unit == target_unit or target_unit in unit_alias_list):
                target_found = True
                key = f"A1{unit_alias_string}"
                formatted_results[key] = f"{value:.4f} {abbr}"
            else:
                key = unit_alias_string
                formatted_results[key] = f"{value:.4f} {abbr}"

    if target_unit and not target_found:
        for unit, abbr in unit_order[measurement_type]:
            unit_alias_list = aliases.get(unit, [unit])
            if target_unit.lower() in [alias.lower() for alias in unit_alias_list] or target_unit.lower() == abbr.lower():
                if unit in conversions:
                    value = conversions[unit]
                    unit_alias_string = ' '.join(unit_alias_list)
                    key = f"A1{unit_alias_string}"
                    formatted_results[key] = f"{value:.4f} {abbr}"
                    break

    return formatted_results