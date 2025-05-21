import re
from flask import jsonify

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
    pattern = r'([-+]?\d*\.?\d+)\s*([a-zA-Z]+\.?|[a-zA-Z]+\s*[a-zA-Z]+|°[a-zA-Z])'
    match = re.match(pattern, input_text)

    if not match:
        return None

    value = float(match.group(1))
    unit = match.group(2).lower().strip()

    unit_mapping = {
        'ft': 'feet', 'foot': 'feet', 'feet': 'feet', "'": 'feet',
        'in': 'inches', 'inch': 'inches', 'inches': 'inches', '"': 'inches',
        'yd': 'yards', 'yard': 'yards', 'yards': 'yards',
        'mi': 'miles', 'mile': 'miles', 'miles': 'miles',
        'm': 'meters', 'meter': 'meters', 'meters': 'meters', 'metre': 'meters', 'metres': 'meters',
        'cm': 'centimeters', 'centimeter': 'centimeters', 'centimeters': 'centimeters',
        'mm': 'millimeters', 'millimeter': 'millimeters', 'millimeters': 'millimeters',
        'km': 'kilometers', 'kilometer': 'kilometers', 'kilometers': 'kilometers',
        'dm': 'decimeters', 'decimeter': 'decimeters', 'decimeters': 'decimeters',
        'dam': 'dekameters', 'dekameter': 'dekameters', 'dekameters': 'dekameters',
        'hm': 'hectometers', 'hectometer': 'hectometers', 'hectometers': 'hectometers',
        'μm': 'micrometers', 'micrometer': 'micrometers', 'micrometers': 'micrometers', 'micron': 'micrometers',
        'nm': 'nanometers', 'nanometer': 'nanometers', 'nanometers': 'nanometers',
        'pm': 'picometers', 'picometer': 'picometers', 'picometers': 'picometers',
        'au': 'astronomical units', 'astronomical unit': 'astronomical units',
        'ly': 'light years', 'light year': 'light years', 'light-year': 'light years',

        'g': 'grams', 'gram': 'grams', 'grams': 'grams',
        'kg': 'kilograms', 'kilogram': 'kilograms', 'kilograms': 'kilograms',
        'mg': 'milligrams', 'milligram': 'milligrams', 'milligrams': 'milligrams',
        'μg': 'micrograms', 'microgram': 'micrograms', 'micrograms': 'micrograms',
        'ng': 'nanograms', 'nanogram': 'nanograms', 'nanograms': 'nanograms',
        'pg': 'picograms', 'picogram': 'picograms', 'picograms': 'picograms',
        'dg': 'decigrams', 'decigram': 'decigrams', 'decigrams': 'decigrams',
        'dag': 'dekagrams', 'dekagram': 'dekagrams', 'dekagrams': 'dekagrams',
        'hg': 'hectograms', 'hectogram': 'hectograms', 'hectograms': 'hectograms',
        'lb': 'pounds', 'lbs': 'pounds', 'pound': 'pounds', 'pounds': 'pounds',
        'oz': 'ounces', 'ounce': 'ounces', 'ounces': 'ounces',
        'st': 'stones', 'stone': 'stones', 'stones': 'stones',
        't': 'tonnes', 'ton': 'tonnes', 'metric ton': 'tonnes', 'tonnes': 'tonnes',
        'ct': 'carats', 'carat': 'carats', 'carats': 'carats',
        'gr': 'grains', 'grain': 'grains', 'grains': 'grains',
        'dwt': 'pennyweights', 'pennyweight': 'pennyweights', 'pennyweights': 'pennyweights',

        'l': 'liters', 'liter': 'liters', 'liters': 'liters', 'litre': 'liters', 'litres': 'liters',
        'ml': 'milliliters', 'milliliter': 'milliliters', 'milliliters': 'milliliters',
        'cl': 'centiliters', 'centiliter': 'centiliters', 'centiliters': 'centiliters',
        'dl': 'deciliters', 'deciliter': 'deciliters', 'deciliters': 'deciliters',
        'dal': 'dekaliters', 'dekaliter': 'dekaliters', 'dekaliters': 'dekaliters',
        'hl': 'hectoliters', 'hectoliter': 'hectoliters', 'hectoliters': 'hectoliters',
        'kl': 'kiloliters', 'kiloliter': 'kiloliters', 'kiloliters': 'kiloliters',
        'μl': 'microliters', 'microliter': 'microliters', 'microliters': 'microliters',
        'nl': 'nanoliters', 'nanoliter': 'nanoliters', 'nanoliters': 'nanoliters',
        'pl': 'picoliters', 'picoliter': 'picoliters', 'picoliters': 'picoliters',
        'gal': 'gallons', 'gallon': 'gallons', 'gallons': 'gallons',
        'qt': 'quarts', 'quart': 'quarts', 'quarts': 'quarts',
        'pt': 'pints', 'pint': 'pints', 'pints': 'pints',
        'c': 'cups', 'cup': 'cups', 'cups': 'cups',
        'floz': 'fluid ounces', 'fl oz': 'fluid ounces', 'fluid ounce': 'fluid ounces', 'fluid ounces': 'fluid ounces',
        'tbsp': 'tablespoons', 'tablespoon': 'tablespoons', 'tablespoons': 'tablespoons',
        'tsp': 'teaspoons', 'teaspoon': 'teaspoons', 'teaspoons': 'teaspoons',
        'bbl': 'barrels', 'barrel': 'barrels', 'barrels': 'barrels',

        'ft³': 'cubic feet', 'cu ft': 'cubic feet', 'cubic feet': 'cubic feet', 'ft3': 'cubic feet',
        'in³': 'cubic inches', 'cu in': 'cubic inches', 'cubic inches': 'cubic inches', 'in3': 'cubic inches',
        'yd³': 'cubic yards', 'cu yd': 'cubic yards', 'cubic yards': 'cubic yards', 'yd3': 'cubic yards',
        'm³': 'cubic meters', 'cu m': 'cubic meters', 'cubic meters': 'cubic meters', 'm3': 'cubic meters',
        'cm³': 'cubic centimeters', 'cu cm': 'cubic centimeters', 'cubic centimeters': 'cubic centimeters', 'cm3': 'cubic centimeters', 'cc': 'cubic centimeters',
        'mm³': 'cubic millimeters', 'cu mm': 'cubic millimeters', 'cubic millimeters': 'cubic millimeters', 'mm3': 'cubic millimeters',
        'km³': 'cubic kilometers', 'cu km': 'cubic kilometers', 'cubic kilometers': 'cubic kilometers', 'km3': 'cubic kilometers',
        'dm³': 'cubic decimeters', 'cu dm': 'cubic decimeters', 'cubic decimeters': 'cubic decimeters', 'dm3': 'cubic decimeters',
        'dam³': 'cubic dekameters', 'cu dam': 'cubic dekameters', 'cubic dekameters': 'cubic dekameters', 'dam3': 'cubic dekameters',
        'hm³': 'cubic hectometers', 'cu hm': 'cubic hectometers', 'cubic hectometers': 'cubic hectometers', 'hm3': 'cubic hectometers',

        'b': 'bits', 'bit': 'bits', 'bits': 'bits',
        'kb': 'kilobits', 'kilobit': 'kilobits', 'kilobits': 'kilobits',
        'mb': 'megabits', 'megabit': 'megabits', 'megabits': 'megabits',
        'gb': 'gigabits', 'gigabit': 'gigabits', 'gigabits': 'gigabits',
        'tb': 'terabits', 'terabit': 'terabits', 'terabits': 'terabits',
        'pb': 'petabits', 'petabit': 'petabits', 'petabits': 'petabits',
        'byte': 'bytes', 'bytes': 'bytes',
        'kib': 'kibibytes', 'kibibyte': 'kibibytes', 'kibibytes': 'kibibytes',
        'mib': 'mebibytes', 'mebibyte': 'mebibytes', 'mebibytes': 'mebibytes',
        'gib': 'gibibytes', 'gibibyte': 'gibibytes', 'gibibytes': 'gibibytes',
        'tib': 'tebibytes', 'tebibyte': 'tebibytes', 'tebibytes': 'tebibytes',
        'pib': 'pebibytes', 'pebibyte': 'pebibytes', 'pebibytes': 'pebibytes',
        'kb_decimal': 'kilobytes decimal', 'kilobyte': 'kilobytes decimal', 'kilobytes': 'kilobytes decimal',
        'mb_decimal': 'megabytes decimal', 'megabyte': 'megabytes decimal', 'megabytes': 'megabytes decimal',
        'gb_decimal': 'gigabytes decimal', 'gigabyte': 'gigabytes decimal', 'gigabytes': 'gigabytes decimal',
        'tb_decimal': 'terabytes decimal', 'terabyte': 'terabytes decimal', 'terabytes': 'terabytes decimal',
        'pb_decimal': 'petabytes decimal', 'petabyte': 'petabytes decimal', 'petabytes': 'petabytes decimal',

        '°c': 'celsius', 'celsius': 'celsius', 'c': 'celsius',
        '°f': 'fahrenheit', 'fahrenheit': 'fahrenheit', 'f': 'fahrenheit',
        '°k': 'kelvin', 'kelvin': 'kelvin', 'k': 'kelvin',
        '°r': 'rankine', 'rankine': 'rankine', 'r': 'rankine'
    }

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
                'barrels': 119.24
            }
        },
        'cubic_volume': {
            'cubic_meters': {
                'cubic feet': 0.0283168, 'cubic inches': 0.0000163871, 'cubic yards': 0.764555,
                'cubic meters': 1, 'cubic centimeters': 0.000001, 'cubic millimeters': 0.000000001,
                'cubic kilometers': 1000000000, 'cubic decimeters': 0.001, 'cubic dekameters': 1000,
                'cubic hectometers': 1000000
            }
        },
        'data_bits': {
            'bits': {
                'bits': 1, 'kilobits': 1000, 'megabits': 1000000, 'gigabits': 1000000000,
                'terabits': 1000000000000, 'petabits': 1000000000000000
            }
        },
        'data_bytes': {
            'bytes': {
                'bytes': 1, 'kibibytes': 1024, 'mebibytes': 1048576, 'gibibytes': 1073741824,
                'tebibytes': 1099511627776, 'pebibytes': 1125899906842624,
                'kilobytes decimal': 1000, 'megabytes decimal': 1000000, 'gigabytes decimal': 1000000000,
                'terabytes decimal': 1000000000000, 'petabytes decimal': 1000000000000000
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
            'dekaliters': 10, 'hectoliters': 100, 'kiloliters': 1000, 'barrels': 119.24
        },
        'cubic_volume': {
            'cubic inches': 0.0000163871, 'cubic feet': 0.0283168, 'cubic yards': 0.764555,
            'cubic millimeters': 0.000000001, 'cubic centimeters': 0.000001, 'cubic decimeters': 0.001,
            'cubic meters': 1, 'cubic dekameters': 1000, 'cubic hectometers': 1000000,
            'cubic kilometers': 1000000000
        },
        'data_bits': {
            'bits': 1, 'kilobits': 1000, 'megabits': 1000000, 'gigabits': 1000000000,
            'terabits': 1000000000000, 'petabits': 1000000000000000
        },
        'data_bytes': {
            'bytes': 1, 'kibibytes': 1024, 'mebibytes': 1048576, 'gibibytes': 1073741824,
            'tebibytes': 1099511627776, 'pebibytes': 1125899906842624,
            'kilobytes decimal': 1000, 'megabytes decimal': 1000000, 'gigabytes decimal': 1000000000,
            'terabytes decimal': 1000000000000, 'petabytes decimal': 1000000000000000
        },
        'temperature': {
            'celsius': 1, 'fahrenheit': 1, 'kelvin': 1, 'rankine': 1
        }
    }

    if measurement_type == 'temperature':
        return {unit: convert_celsius_to_unit(base_value, unit) for unit in conversion_factors[measurement_type]}
    else:
        return {unit: base_value / factor for unit, factor in conversion_factors[measurement_type].items()}

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
            ('kiloliters', 'kL'), ('barrels', 'bbl')
        ],
        'cubic_volume': [
            ('cubic inches', 'in³'), ('cubic feet', 'ft³'), ('cubic yards', 'yd³'),
            ('cubic millimeters', 'mm³'), ('cubic centimeters', 'cm³'),
            ('cubic decimeters', 'dm³'), ('cubic meters', 'm³'),
            ('cubic dekameters', 'dam³'), ('cubic hectometers', 'hm³'),
            ('cubic kilometers', 'km³')
        ],
        'data_bits': [
            ('bits', 'b (Bits)'), ('kilobits', 'Kb (Bits)'), ('megabits', 'Mb (Bits)'),
            ('gigabits', 'Gb (Bits)'), ('terabits', 'Tb (Bits)'), ('petabits', 'Pb (Bits)')
        ],
        'data_bytes': [
            ('bytes', 'B (Bytes)'), ('kibibytes', 'KiB (Bytes)'), ('mebibytes', 'MiB (Bytes)'),
            ('gibibytes', 'GiB (Bytes)'), ('tebibytes', 'TiB (Bytes)'), ('pebibytes', 'PiB (Bytes)'),
            ('kilobytes decimal', 'KB (Bytes)'), ('megabytes decimal', 'MB (Bytes)'),
            ('gigabytes decimal', 'GB (Bytes)'), ('terabytes decimal', 'TB (Bytes)'),
            ('petabytes decimal', 'PB (Bytes)')
        ],
        'temperature': [
            ('celsius', '°C'), ('fahrenheit', '°F'), ('kelvin', 'K'), ('rankine', '°R')
        ]
    }

    formatted_results = {}
    target_found = False
    target_key = None

    for idx, (unit, abbr) in enumerate(unit_order[measurement_type], 1):
        if unit in conversions:
            value = conversions[unit]
            key = f"unit{idx}"

            if target_unit and unit == target_unit:
                target_found = True
                target_key = f"A1unit{idx}"
                formatted_results[target_key] = f"{value:.4f} {abbr}"
            else:
                formatted_results[key] = f"{value:.4f} {abbr}"

    if target_unit and not target_found:
        for unit, abbr in unit_order[measurement_type]:
            if target_unit.lower() in unit.lower() or target_unit.lower() == abbr.lower():
                if unit in conversions:
                    value = conversions[unit]
                    target_key = "A1unit1"
                    formatted_results[target_key] = f"{value:.4f} {abbr}"
                    break

    return formatted_results