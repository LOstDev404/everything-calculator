from flask import jsonify
from fractions import Fraction
#Fraction percent convert

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


#Shape names
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