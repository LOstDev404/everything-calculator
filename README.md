# everything-calculator
A collection of tools/calculators.

The project is a hosted on its [Flask Site](https://everything-calculator.vercel.app/)


## List of Calculators:
Here’s a breakdown of the calculators currently included (Sorted by most recently added on top):

- Area/Perimeter | Circle and Regular Polygons
- Algebra | Two Step Equations
- Patterns | Arithmetic and Geometric Sequences
- Trigonometry (Right Triangle) + Pythagorean Theorem

## Contributing:
1. Fork the repository and clone it locally.
2. Make your changes
3. Submit a pull request with your improvements.

### Contribution Guidelines:
- Make sure you aren't creating a duplicate calculator.
- Use either camelCase or snake_case.
- Make sure you use the right naming convention in commit messages

### Version Naming Convention:
The project uses a three-digit versioning format: `0.XYZ`

- **X (ones place)** – Major structural changes, like large file reorganizations/logic updates.
- 
- **Y (tenths place)** – New calculator/page additions.
- 
- **Z (hundredths place)** – Minor changes, such as grammar fixes or small bug fixes in calculators.  

Once a digit exceeds 9, it rolls over to the next place (ex: `0.249` -> `0.250`).

## Support:
If you find a bug or have a feature request, please feel free to open an issue in the repository!

## Calculator Creation:
1. Create a `{calculator}.py` file for your calculator. (Ex: `examplecalculator.py`)
2. Add your calculator to the [`calculators.json`](calculators.json) file:

    ```json
   {
       "id": "examplecalculator", 
       "name": "Example Calculator | For the README",
       "description": "An example calculator",
       "tags": "calculator example calculator ex readme",
       "title": "Example Calculator:",
       "subtitle": "Fill all of the boxes and select an option",
       "selectorinput": {
            "exampleOptions": {
                "label": "Select an option:",
                "options": {
                    "optionOne": "Option One",
                    "optionOne": "Option Two"
                }
            }
        },
       "numberinput": {
           "numberInput1": "Example number input 1:",
           "numberInput2": "Example number input 2:",

       },
        "testinput": {
            "textInput1": "Example text input 1:",
            "textInput2": "Example text input 2:",

        }
   },
   ```
   `Note: Subtitles aren't required`
   
4. Create the code for the calculation in your Python file
5. Have results returned by creating the `result` using `jsonify`, and make sure to return it properly:

    ```python
    result = jsonify({
        'values': {
            'value1': f"Value #1: {value1}",
            'value2': f"Value #2: {value2}"
        }
    })
    return result
    ```
6. Sumbit a pull request with your calculator and wait for it to be Approved and Merged. 