document.addEventListener('DOMContentLoaded', function() {
  const calculatorForm = document.getElementById('calculatorForm');
  const errorMessage = document.getElementById('error-message');
  const calculatedValues = document.getElementById('calculated-values');
  const plot = document.getElementById('plot')

  if (calculatorForm) {
    calculatorForm.addEventListener('submit', async function(e) {
      e.preventDefault();

      const formData = {};
      const formElements = calculatorForm.elements;
      for (let i = 0; i < formElements.length; i++) {
        const element = formElements[i];
        if (element.tagName === 'INPUT' && element.type !== 'submit') {
          formData[element.id] = element.value;
        }
        if (element.tagName === 'SELECT') {
          formData[element.id] = element.options[element.selectedIndex].value;
        }
      }

        try {
          const slug = window.location.pathname.split('/')[1];
          const response = await fetch(`/${slug}_calculate`, {
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
          const plots = document.querySelectorAll('[id*="plot"]');
          plots.forEach(plot => {
              plot.style.display = 'none';
          });
          calculatedValues.innerHTML = '';
        } else {
          const plots = document.querySelectorAll('[id*="plot"]');
          plots.forEach(plot => {
              plot.src = `data:image/png;base64,${data.plot}`;
              plot.style.width = '80%';
              plot.style.height = 'auto';
              plot.style.display = 'block';
          });
          errorMessage.style.display = 'none';

          const elementsData = Object.keys(data.values).map(key => ({
            id: `${key}-text`,
            value: data.values[key]
          }));

          calculatedValues.innerHTML = elementsData.map(item => `
            <div class="results-container">
              <p id="${item.id}">${item.value}</p>
              <button type="button" class="copy-btn" data-target="#${item.id}"><i data-feather="copy"></i></button>
            </div>
          `).join('');

          feather.replace();
        }

      } catch (error) {
        errorMessage.style.display = 'block';
        errorMessage.textContent = 'An error occurred while calculating';
        const plots = document.querySelectorAll('[id*="plot"]');
        plots.forEach(plot => {
          plot.style.display = 'none';
        });
        calculatedValues.innerHTML = '';
      }
    });
  }
});