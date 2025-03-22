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
                    <p>Shape: ${data.values.shape}</p>
                    <p>Area: ${data.values.areaFrac}</p>
                    <p>${data.values.perimeterFrac}</p>
                    <p>${data.values.radiusDiameterInterior}</p>
                  `;
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