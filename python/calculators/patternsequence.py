from flask import jsonify
from python.utils import float_to_fraction_percent
def patternsequence_solve(data):
    try:
        operation = data['sequenceType']
        firstTerm = float(data['firstTerm'])
        secondTerm = float(data['secondTerm'])
        lastTerm = float(data['lastTerm'])

        if operation == 'add_sub':
            lastTermCalculated = ((lastTerm - 1) * (secondTerm-firstTerm)) + firstTerm
        elif operation == 'mult_div':
            commonRatio = secondTerm / firstTerm

            lastTermCalculated = firstTerm * (commonRatio ** (lastTerm - 1))
        else:
            return jsonify({'error': 'Failed to calculate...'})
            
            
        return jsonify({
            'values': {
                'lastTermCalculated': f"Term {lastTerm:.3} is {lastTermCalculated:.3f}",
                'lastTermCalculatedFrac': f"Term {lastTerm} is {float_to_fraction_percent(lastTermCalculated)}"
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)})
        