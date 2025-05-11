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
                    <div class="results-container">
                        <p id="angle1-text">${data.values.angle1}</p>
                        <button type="button" class="copy-btn" data-target="#angle1-text"><i data-feather="copy"></i></button>
                    </div>
                    <div class="results-container">
                        <p id="angle2-text">${data.values.angle2}</p>
                        <button type="button" class="copy-btn" data-target="#angle2-text"><i data-feather="copy"></i></button>
                    </div>
                    <div class="results-container">
                        <p id="adjacent-text">${data.values.adjacent}</p>
                        <button type="button" class="copy-btn" data-target="#adjacent-text"><i data-feather="copy"></i></button>
                    </div>
                    <div class="results-container">
                        <p id="opposite-text">${data.values.opposite}</p>
                        <button type="button" class="copy-btn" data-target="#opposite-text"><i data-feather="copy"></i></button>
                    </div>
                    <div class="results-container">
                        <p id="hypotenuse-text">${data.values.hypotenuse}</p>
                        <button type="button" class="copy-btn" data-target="#hypotenuse-text"><i data-feather="copy"></i></button>
                    </div>
                    <div class="results-container">
                        <p id="perimeter-text">${data.values.perimeter}</p>
                        <button type="button" class="copy-btn" data-target="#perimeter-text"><i data-feather="copy"></i></button>
                    </div>
                    <div class="results-container">
                        <p id="area-text">${data.values.area}</p>
                        <button type="button" class="copy-btn" data-target="#area-text"><i data-feather="copy"></i></button>
                    </div>
                `;
                feather.replace();
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