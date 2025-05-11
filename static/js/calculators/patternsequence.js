document.addEventListener('DOMContentLoaded', function() {
  const calculatorForm = document.getElementById('calculatorForm');
  const errorMessage = document.getElementById('error-message');
  const calculatedValues = document.getElementById('calculated-values');
  const clearButton = document.getElementById('clearButton');
    
  if (calculatorForm) {
        calculatorForm.addEventListener('submit', async function(e) {
          e.preventDefault();

          const formData = {
              operation: document.getElementById('operation').value,
              firstTerm: document.getElementById('firstTerm').value,
              secondTerm: document.getElementById('secondTerm').value,
              lastTerm: document.getElementById('lastTerm').value
          };

          try {
              const response = await fetch('/patternsequence_calculate', {
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
                    <p id="lastTermCalculated-text">${data.values.lastTermCalculated}</p>
                    <button type="button" class="copy-btn" data-target="#lastTermCalculated-text"><i data-feather="copy"></i></button>
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
              document.getElementById('firstTerm').value = '';
              document.getElementById('secondTerm').value = '';
              document.getElementById('lastTerm').value = '';

          });
      }
  
});