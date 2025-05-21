document.addEventListener('DOMContentLoaded', function() {
  console.log('calculator.js loaded');
  document.addEventListener('calculatorLoaded', initializeCalculatorForm);

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

  initializeClearButtons();
}

async function handleFormSubmit(e) {
  e.preventDefault();
  const calculatorForm = e.target;
  const errorMessage = document.getElementById('error-message');
  const calculatedValues = document.getElementById('calculated-values');

  calculatedValues.innerHTML = '<p style="max-height: 2.5em;;">Calculating...</p>';
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
        const entries = Object.entries(data.values);
        const decimalEntries = entries.filter(([key]) => !key.toLowerCase().includes('frac'));
        const fractionEntries = entries.filter(([key]) => key.toLowerCase().includes('frac'));
        const totalResults = entries.length;
        const RESULTS_THRESHOLD = 13;
        
        if (totalResults > RESULTS_THRESHOLD) {
          const searchContainer = document.createElement('div');
          searchContainer.className = 'results-search-container';
          searchContainer.style.marginBottom = '1em';
          
          const searchInput = document.createElement('input');
          searchInput.type = 'text';
          searchInput.className = 'search-input';
          searchInput.placeholder = 'Search results...';
          
          
          searchContainer.appendChild(searchInput);
          calculatedValues.appendChild(searchContainer);
          searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const resultRows = document.querySelectorAll('.results-container');
            
            resultRows.forEach(row => {
              const textElement = row.querySelector('p');
              const keyId = textElement.id.replace('-text', '');
              const textContent = textElement.textContent.toLowerCase();
              
              if (keyId.toLowerCase().includes(searchTerm) || textContent.includes(searchTerm)) {
                row.style.display = 'flex';
              } else {
                row.style.display = 'none';
              }
            });
            
            document.querySelectorAll('.category-container').forEach(category => {
              const categoryResults = category.querySelectorAll('.results-container');
              const visibleResults = Array.from(categoryResults).filter(row => row.style.display !== 'none');
              
              if (visibleResults.length === 0) {
                category.querySelector('h3').style.display = 'none';
              } else {
                category.querySelector('h3').style.display = 'block';
              }
            });
          });
        }

        function makeResultRow(key, val) {
          const container = document.createElement('div');
          container.className = 'results-container';
          container.style.marginBottom = '0.5em';
          container.dataset.key = key;
          container.dataset.value = val;

          const p = document.createElement('p');
          p.id = `${key}-text`;
          p.textContent = val;

          const btn = document.createElement('button');
          btn.type = 'button';
          btn.className = 'copy-btn';
          btn.setAttribute('data-target', `#${key}-text`);
          btn.innerHTML = `<i data-feather="copy"></i>`;

          container.append(p, btn);
          return container;
        }

        if (decimalEntries.length === 0 || fractionEntries.length === 0) {
          entries.forEach(([key, val]) =>
            calculatedValues.appendChild(makeResultRow(key, val))
          );
        } else {
          const makeCategory = (title, items) => {
            const div = document.createElement('div');
            div.className = 'category-container';

            const h3 = document.createElement('h3');
            h3.textContent = title;
            h3.style.fontFamily = "'Roboto', sans-serif";
            div.appendChild(h3);

            items.forEach(([key, val]) =>
              div.appendChild(makeResultRow(key, val))
            );
            return div;
          };

          const decimalsTitle = decimalEntries.length === 1 ? 'Decimal:' : 'Decimals:';
          const fractionsTitle = fractionEntries.length === 1 ? 'Fraction:' : 'Fractions:';

          calculatedValues.appendChild(
            makeCategory(decimalsTitle, decimalEntries)
          );
          calculatedValues.appendChild(
            makeCategory(fractionsTitle, fractionEntries)
          );
        }

        if (window.feather) feather.replace();
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