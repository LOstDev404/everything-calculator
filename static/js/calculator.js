document.addEventListener('DOMContentLoaded', function() {
  console.log('calculator.js loaded');

  // Initialize form event listeners once the calculator data is loaded
  document.addEventListener('calculatorLoaded', initializeCalculatorForm);

  // Set up event delegation for buttons that might be dynamically added
  setupButtonEventDelegation();
});

function initializeCalculatorForm() {
  const calculatorForm = document.getElementById('calculatorForm');
  const errorMessage = document.getElementById('error-message');
  const calculatedValues = document.getElementById('calculated-values');

  if (calculatorForm) {
    console.log('Form found');
    calculatorForm.addEventListener('submit', handleFormSubmit);
  }

  // Initialize clear buttons that are now in the DOM
  initializeClearButtons();
}

async function handleFormSubmit(e) {
  e.preventDefault();
  const calculatorForm = e.target;
  const errorMessage = document.getElementById('error-message');
  const calculatedValues = document.getElementById('calculated-values');

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
    const slug = window.location.pathname.split('/')[2];
    console.log(slug)
    const response = await fetch(`/calculators/solve/${slug}`, {
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
      errorMessage.style.display = 'none';

      calculatedValues.innerHTML = '';

      if (data.plot) {
        const visualizationSection = document.createElement('div');
        visualizationSection.id = 'visualization-section';

        const plotImg = document.createElement('img');
        plotImg.id = 'plot';
        plotImg.src = `data:image/png;base64,${data.plot}`;
        plotImg.alt = 'Visualization';
        plotImg.style.width = '80%';
        plotImg.style.height = 'auto';
        plotImg.style.display = 'block';

        visualizationSection.appendChild(plotImg);
        calculatedValues.appendChild(visualizationSection);
      }

      if (data.values) {
        Object.keys(data.values).forEach(key => {
          const resultsContainer = document.createElement('div');
          resultsContainer.className = 'results-container';

          const valuePara = document.createElement('p');
          valuePara.id = `${key}-text`;
          valuePara.textContent = data.values[key];

          const copyButton = document.createElement('button');
          copyButton.type = 'button';
          copyButton.className = 'copy-btn';
          copyButton.setAttribute('data-target', `#${key}-text`);

          const copyIcon = document.createElement('i');
          copyIcon.setAttribute('data-feather', 'copy');
          copyButton.appendChild(copyIcon);

          resultsContainer.appendChild(valuePara);
          resultsContainer.appendChild(copyButton);
          calculatedValues.appendChild(resultsContainer);
        });

        if (window.feather) {
          feather.replace();
        }
      }
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
}

function initializeClearButtons() {
  document.querySelectorAll('.clear-single-btn').forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      const targetId = this.getAttribute('data-target');
      if (targetId) {
        const input = document.getElementById(targetId);
        if (input) {
          input.value = '';
        }
      }
    });
  });

  const clearButton = document.querySelector('.clear-btn');
  if (clearButton) {
    clearButton.addEventListener('click', function(e) {
      e.preventDefault();
      const allInputs = document.querySelectorAll('input');
      allInputs.forEach(input => input.value = '');
    });
  }
}

function setupButtonEventDelegation() {
  document.addEventListener('click', function(event) {
    if (event.target.matches('.copy-btn') || event.target.closest('.copy-btn')) {
      const button = event.target.matches('.copy-btn') ? event.target : event.target.closest('.copy-btn');

      document.querySelectorAll('.copy-btn').forEach(btn => {
        if (btn !== button) {
          btn.innerHTML = '<i data-feather="copy"></i>';
          if (window.feather) {
            feather.replace({ scope: btn });
          }
        }
      });

      const targetId = button.getAttribute('data-target');
      const container = document.querySelector(targetId);
      const textToCopy = container.textContent;

      navigator.clipboard.writeText(textToCopy)
        .then(() => {
          button.innerHTML = '<i data-feather="check"></i>';
          if (window.feather) {
            feather.replace({ scope: button });
          }
        })
        .catch(err => {
          console.error('Clipboard write failed', err);
        });
    }
  });
}