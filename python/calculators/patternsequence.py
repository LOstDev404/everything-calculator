from flask import jsonify

def patternsequence_solve(data):
    try:
        operation = data['operation']
        firstTerm = float(data['firstTerm'])
        secondTerm = float(data['secondTerm'])
        lastTerm = float(data['lastTerm'])

        if operation == 'add_sub':
            lastTermCalculated = ((lastTerm - 1) * (secondTerm-firstTerm)) + firstTerm
        elif operation == 'mult_div':
            commonRatio = secondTerm / firstTerm

            lastTermCalculated = firstTerm * (commonRatio ** (lastTerm - 1))
        else:
            result = jsonify({'error': 'Failed to calculate...'})
            return result
            
        result = jsonify({
            'values': {
                'lastTerm': f"{lastTerm:.3f}",
                'lastTermCalculated': f"{lastTermCalculated:.3f}",
            }
        })
        return result
        
    except Exception as e:
        result = jsonify({'error': str(e)})
        
    