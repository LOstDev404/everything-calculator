document.addEventListener('DOMContentLoaded', function() {
  const algebra2stepForm = document.getElementById('algebra2stepForm');
  const errorMessage = document.getElementById('error-message');
  const trianglePlot = document.getElementById('triangle-plot');
  const calculatedValues = document.getElementById('calculated-values');
  const algebra2stepClearButton = document.getElementById('algebra2stepClearButton');

  if (algebra2stepForm) {
      algebra2stepForm.addEventListener('submit', async function(e) {
          e.preventDefault();

          const formData = {
                  algebra2stepequation: document.getElementById('algebra2stepequation').value,

          };
          try {
              const response = await fetch('/algebra2stepcalculate', {
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
                      <p>${data.values.letter} = ${data.values.solution}</p>
                  `;
              }
          } catch (error) {
              errorMessage.style.display = 'block';
              errorMessage.textContent = 'An error occurred while calculating';
              calculatedValues.innerHTML = '';
          }
      });
  }

  if (algebra2stepClearButton) {
      algebra2stepClearButton.addEventListener('click', function(e) {
          e.preventDefault();
          const algebraInput = document.getElementById('algebra2stepequation');
          if (algebraInput) {
              algebraInput.value = '';
              errorMessage.style.display = 'none';
          }
      });
  }


  
});