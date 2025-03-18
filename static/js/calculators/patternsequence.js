document.addEventListener('DOMContentLoaded', function() {
  const patternForm = document.getElementById('patternForm');
  const errorMessage = document.getElementById('error-message');
  const trianglePlot = document.getElementById('triangle-plot');
  const calculatedValues = document.getElementById('calculated-values');
  const patternClearButton = document.getElementById('patternClearButton');
  if (patternClearButton) {
      patternClearButton.addEventListener('click', function(e) {
          e.preventDefault();
          document.getElementById('firstTerm').value = '';
          document.getElementById('secondTerm').value = '';
          document.getElementById('lastTerm').value = '';

      });
  }
  
  if (patternForm) {
      patternForm.addEventListener('submit', async function(e) {
          e.preventDefault();

          const formData = {
              operation: document.getElementById('operation').value,
              firstTerm: document.getElementById('firstTerm').value,
              secondTerm: document.getElementById('secondTerm').value,
              lastTerm: document.getElementById('lastTerm').value
          };

          try {
              const response = await fetch('/patternsequencecalculate', {
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
                  if (patternPlot) {
                      patternPlot.style.display = 'none';
                  }
                  calculatedValues.innerHTML = '';
              } else {
                  errorMessage.style.display = 'none';
                  calculatedValues.innerHTML = `
                      <p>Term ${data.values.lastTerm} is ${data.values.lastTermCalculated}</p>
                  `;
              }
          } catch (error) {
              errorMessage.style.display = 'block';
              errorMessage.textContent = 'An error occurred while calculating';
              calculatedValues.innerHTML = '';
          }
      });
  }
  
});