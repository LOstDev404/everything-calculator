document.addEventListener('DOMContentLoaded', function() {
  const calculatorForm = document.getElementById('calculatorForm');
  const errorMessage = document.getElementById('error-message');
  const calculatedValues = document.getElementById('calculated-values');
  const clearButton = document.getElementById('clearButton');

  if (calculatorForm) {
      calculatorForm.addEventListener('submit', async function(e) {
          e.preventDefault();

          const formData = {
                  algebra2stepequation: document.getElementById('algebra2stepequation').value,

          };
          try {
              const response = await fetch('/algebra2step_calculate', {
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
                    <p id="solution-text">${data.values.solution}</p>
                    <button type="button" class="copy-btn" data-target="#solution-text"><i data-feather="copy"></i></button>
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
          const algebraInput = document.getElementById('algebra2stepequation');
          if (algebraInput) {
              algebraInput.value = '';
              errorMessage.style.display = 'none';
          }
      });
  }


  
});