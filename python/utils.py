from flask import jsonify
from fractions import Fraction

def float_to_fraction_percent(value, suffix="", usepercent=False, purefrac=False, accuracy=1e-8):
    is_fraction_input = isinstance(value, Fraction) or (isinstance(value, str) and '/' in value)
    if isinstance(value, str) and '/' in value:
        parts = value.split('/')
        value = float(int(parts[0]) / int(parts[1]))
    elif isinstance(value, Fraction):
        value = float(value)
    fraction = Fraction(value).limit_denominator()
    pure_fraction = f"{fraction.numerator}/{fraction.denominator}"
    if fraction.denominator == 1:
        fraction_result = f"{fraction.numerator}/1"
    else:
        whole_number = fraction.numerator // fraction.denominator
        remainder = fraction.numerator % fraction.denominator
        if whole_number == 0:
            fraction_result = f"{remainder}/{fraction.denominator}"
        else:
            fraction_result = f"{whole_number} {remainder}/{fraction.denominator}"
    percentage_result = round(value * 100, 3)
    if is_fraction_input:
        primary_result = f"{value:.3f}{suffix}"  
    else:
        primary_result = f"{pure_fraction}{suffix}"  
    if purefrac:
        if is_fraction_input:
            decimal_part = f"{value:.3f}{suffix}"
            fraction_part = f"{fraction_result}{suffix}"
        else:
            decimal_part = f"{value:.3f}{suffix}"
            fraction_part = f"{fraction_result}{suffix}"
        if usepercent:
            percent_part = f"{percentage_result:.3f}{suffix}%"
            return f"{primary_result} | {decimal_part} | {fraction_part} | {percent_part}", pure_fraction
        else:
            return f"{primary_result} | {decimal_part} | {fraction_part}", pure_fraction
    else:
        if usepercent:
            percent_part = f"{percentage_result:.3f}%"
            return f"{primary_result} | {percent_part}"
        else:
            return primary_result

def shape_name(sides):
    sides = int(sides)
    shapes = {
      "3": "Triangle",
      "4": "Square",
      "5": "Pentagon",
      "6": "Hexagon",
      "7": "Heptagon",
      "8": "Octagon",
      "9": "Nonagon",
      "10": "Decagon",
      "11": "Hendecagon",
      "12": "Dodecagon",
      "13": "Tridecagon",
      "14": "Tetradecagon",
      "15": "Pentadecagon",
      "16": "Hexadecagon",
      "17": "Heptadecagon",
      "18": "Octadecagon",
      "19": "Enneadecagon",
      "20": "Icosagon",
      "21": "Icosihenagon",
      "22": "Icosidigon",
      "23": "Icositrigon",
      "24": "Icositetragon",
      "25": "Icosipentagon",
      "26": "Icosihexagon",
      "27": "Icosiheptagon",
      "28": "Icosioctagon",
      "29": "Icosienneagon",
      "30": "Triacontagon",
      "31": "Triacontahenagon",
      "32": "Triacontadigon",
      "33": "Triacontatrigon",
      "34": "Triacontatetragon",
      "35": "Triacontapentagon",
      "36": "Triacontahexagon",
      "37": "Triacontaheptagon",
      "38": "Triacontaoctagon",
      "39": "Triacontaenneagon",
      "40": "Tetracontagon",
      "41": "Tetracontahenagon",
      "42": "Tetracontadigon",
      "43": "Tetracontatrigon",
      "44": "Tetracontatetragon",
      "45": "Tetracontapentagon",
      "46": "Tetracontahexagon",
      "47": "Tetracontaheptagon",
      "48": "Tetracontaoctagon",
      "49": "Tetracontaenneagon",
      "50": "Pentacontagon",
      "51": "Pentacontahenagon",
      "52": "Pentacontadigon",
      "53": "Pentacontatrigon",
      "54": "Pentacontatetragon",
      "55": "Pentacontapentagon",
      "56": "Pentacontahexagon",
      "57": "Pentacontaheptagon",
      "58": "Pentacontaoctagon",
      "59": "Pentacontaenneagon",
      "60": "Hexacontagon",
      "61": "Hexacontahenagon",
      "62": "Hexacontadigon",
      "63": "Hexacontatrigon",
      "64": "Hexacontatetragon",
      "65": "Hexacontapentagon",
      "66": "Hexacontahexagon",
      "67": "Hexacontaheptagon",
      "68": "Hexacontaoctagon",
      "69": "Hexacontaenneagon",
      "70": "Heptacontagon",
      "71": "Heptacontahenagon",
      "72": "Heptacontadigon",
      "73": "Heptacontatrigon",
      "74": "Heptacontatetragon",
      "75": "Heptacontapentagon",
      "76": "Heptacontahexagon",
      "77": "Heptacontaheptagon",
      "78": "Heptacontaoctagon",
      "79": "Heptacontaenneagon",
      "80": "Octacontagon",
      "81": "Octacontahenagon",
      "82": "Octacontadigon",
      "83": "Octacontatrigon",
      "84": "Octacontatetragon",
      "85": "Octacontapentagon",
      "86": "Octacontahexagon",
      "87": "Octacontaheptagon",
      "88": "Octacontaoctagon",
      "89": "Octacontaenneagon",
      "90": "Enneacontagon",
      "91": "Enneacontahenagon",
      "92": "Enneacontadigon",
      "93": "Enneacontatrigon",
      "94": "Enneacontatetragon",
      "95": "Enneacontapentagon",
      "96": "Enneacontahexagon",
      "97": "Enneacontaheptagon",
      "98": "Enneacontaoctagon",
      "99": "Enneacontaenneagon",
      "100": "Hectogon"
    }

    if sides < 3:
        return "Invalid Shape"
    elif sides <= 100:
        shape = shapes.get(str(sides))
        return shape if shape else "Unknown Shape"
    else:
        return f'{sides}-gon'

def get_unit_mappings():
    return {
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

        'ft³': 'cubic feet', 'cu ft': 'cubic feet', 'cubic feet': 'cubic feet', 'ft3': 'cubic feet', 'cubic ft': 'cubic feet',
        'in³': 'cubic inches', 'cu in': 'cubic inches', 'cubic inches': 'cubic inches', 'in3': 'cubic inches', 'cubic in': 'cubic inches',
        'yd³': 'cubic yards', 'cu yd': 'cubic yards', 'cubic yards': 'cubic yards', 'yd3': 'cubic yards', 'cubic yd': 'cubic yards',
        'm³': 'cubic meters', 'cu m': 'cubic meters', 'cubic meters': 'cubic meters', 'm3': 'cubic meters', 'cubic m': 'cubic meters',
        'cm³': 'cubic centimeters', 'cu cm': 'cubic centimeters', 'cubic centimeters': 'cubic centimeters', 'cm3': 'cubic centimeters', 'cc': 'cubic centimeters', 'cubic cm': 'cubic centimeters',
        'mm³': 'cubic millimeters', 'cu mm': 'cubic millimeters', 'cubic millimeters': 'cubic millimeters', 'mm3': 'cubic millimeters', 'cubic mm': 'cubic millimeters',
        'km³': 'cubic kilometers', 'cu km': 'cubic kilometers', 'cubic kilometers': 'cubic kilometers', 'km3': 'cubic kilometers', 'cubic km': 'cubic kilometers',
        'dm³': 'cubic decimeters', 'cu dm': 'cubic decimeters', 'cubic decimeters': 'cubic decimeters', 'dm3': 'cubic decimeters', 'cubic dm': 'cubic decimeters',
        'dam³': 'cubic dekameters', 'cu dam': 'cubic dekameters', 'cubic dekameters': 'cubic dekameters', 'dam3': 'cubic dekameters', 'cubic dam': 'cubic dekameters',
        'hm³': 'cubic hectometers', 'cu hm': 'cubic hectometers', 'cubic hectometers': 'cubic hectometers', 'hm3': 'cubic hectometers', 'cubic hm': 'cubic hectometers',

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