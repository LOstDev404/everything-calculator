document.addEventListener('DOMContentLoaded', function() {
  const calculatorForm = document.getElementById('calculatorForm');
  const errorMessage = document.getElementById('error-message');
  const trianglePlot = document.getElementById('triangle-plot');
  const calculatedValues = document.getElementById('calculated-values');
  const clearButton = document.getElementById('clearButton');

  if (calculatorForm) {
    calculatorForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const formData = {
            angle1: document.getElementById('angle1').value,
            adjacent: document.getElementById('adjacent').value,
            opposite: document.getElementById('opposite').value,
            hypotenuse: document.getElementById('hypotenuse').value
        };

        try {
            const response = await fetch('/trigonometrypythagoreantheorem_calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (data.error) {
                errorMessage.style.display = 'block';
                errorMessage.textContent = data.error;
                if (trianglePlot) {
                    trianglePlot.style.display = 'none';
                }
                calculatedValues.innerHTML = '';
            } else {
                errorMessage.style.display = 'none';
                if (trianglePlot) {
                    trianglePlot.src = `data:image/png;base64,${data.plot}`;
                    trianglePlot.style.width = '80%';
                    trianglePlot.style.height = 'auto';
                    trianglePlot.style.display = 'block';
                }
                document.getElementById('angle1').value = data.values.angle1;
                document.getElementById('adjacent').value = data.values.adjacent;
                document.getElementById('opposite').value = data.values.opposite;
                document.getElementById('hypotenuse').value = data.values.hypotenuse;

                calculatedValues.innerHTML = `
                    <h2>Formatting: Decimal | Fraction</h2>
                    <p>Angle 1: ${data.values.angle1frac}</p>
                    <p>Angle 2: ${data.values.angle2frac}</p>
                    <p>Adjacent (A): ${data.values.adjacentfrac}</p>
                    <p>Opposite (B): ${data.values.oppositefrac}</p>
                    <p>Hypotenuse (C): ${data.values.hypotenusefrac}</p>
                    <p>Perimiter: ${data.values.perimiterfrac}</p>
                    <p>Area: ${data.values.areafrac}</p>
                `;
            }
        } catch (error) {
            errorMessage.style.display = 'block';
            errorMessage.textContent = 'An error occurred while generating the triangle';            

            if (trianglePlot) {
                trianglePlot.style.display = 'none';
            }
            calculatedValues.innerHTML = '';
        }
    });
  }

  if (clearButton) {
    clearButton.addEventListener('click', function(e) {
        e.preventDefault();
        document.getElementById('angle1').value = '';
        document.getElementById('adjacent').value = '';
        document.getElementById('opposite').value = '';
        document.getElementById('hypotenuse').value = '';
        errorMessage.style.display = 'none';


    });
  }
});