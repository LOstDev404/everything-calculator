document.addEventListener('DOMContentLoaded', function() {
  const calculatorForm = document.getElementById('calculatorForm');
  const errorMessage = document.getElementById('error-message');
  const calculatedValues = document.getElementById('calculated-values');
  const clearButton = document.getElementById('clearButton');
    
  if (calculatorForm) {
        calculatorForm.addEventListener('submit', async function(e) {
          e.preventDefault();

            const formData = {
                radiusSides: document.getElementById('radiusSides').value,
                diameterLength: document.getElementById('diameterLength').value
              };
          try {
              const response = await fetch('/circlepolygon_calculate', {
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
                  calculatedValues.innerHTML = '';
              } else {
                  errorMessage.style.display = 'none';
                  calculatedValues.innerHTML = `
                    <div class="results-container">
                    <p id="shape-text">${data.values.shape}</p>
                    <button type="button" class="copy-btn" data-target="#shape-text"><i data-feather="copy"></i></button>
                    </div>
                    <div class="results-container">
                    <p id="areaFrac-text">${data.values.areaFrac}</p>
                    <button type="button" class="copy-btn" data-target="#areaFrac-text"><i data-feather="copy"></i></button>
                    </div>
                    <div class="results-container">
                    <p id="perimeterFrac-text">${data.values.perimeterFrac}</p>
                    <button type="button" class="copy-btn" data-target="#perimeterFrac-text"><i data-feather="copy"></i></button>
                    </div>
                    <div class="results-container">
                    <p id="radiusDiameterInterior-text">${data.values.radiusDiameterInterior}</p>
                    <button type="button" class="copy-btn" data-target="#radiusDiameterInterior-text"><i data-feather="copy"></i></button>
                    </div>
                  `;
                  feather.replace();
              }
              
          } catch (error) {
              errorMessage.style.display = 'block';
              errorMessage.textContent = 'An error occurred while calculating';
              calculatedValues.innerHTML = '';
          }
      });
  }

      if (clearButton) {
            clearButton.addEventListener('click', function(e) {
              e.preventDefault();
              document.getElementById('radiusSides').value = '';
              document.getElementById('diameterLength').value = '';

          });
      }
  
});