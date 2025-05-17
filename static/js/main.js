document.addEventListener('DOMContentLoaded', function() {
    initializeSearchHandling();
});
                            
function initializeSearchHandling() {
    const searchInput = document.getElementById('calculatorSearch');
    const calculationResult = document.getElementById('calculationResult');
    let typingTimer;

    if (searchInput) {
        const urlParams = new URLSearchParams(window.location.search);
        const searchParam = urlParams.get('search');

        if (searchParam) {
            searchInput.value = searchParam;

            waitForCardsAndFilter(searchParam.toLowerCase());
        }

        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            clearTimeout(typingTimer);

            if (/[\d\+\-\*\/\(\)x\^]/.test(searchTerm)) {
                typingTimer = setTimeout(async function() {
                    try {
                        const response = await fetch('/calculate', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ expression: searchTerm })
                        });

                        const data = await response.json();
                        if (data.result !== null) {
                            calculationResult.textContent = `= ${data.result}`;
                            calculationResult.style.display = 'block';
                            return;
                        }
                    } catch (error) {
                        console.error('Error calculating:', error);
                    }
                    calculationResult.style.display = 'none';
                }, 100);
            } else {
                calculationResult.style.display = 'none';
            }

            filterAndSortCards(searchTerm);
        });
    }
}

function waitForCardsAndFilter(searchTerm) {

    const checkInterval = setInterval(() => {
        const cards = document.querySelectorAll('.calculator-card-wrapper');
        if (cards.length > 0) {
            clearInterval(checkInterval);
            filterAndSortCards(searchTerm);
        }
    }, 100);

    setTimeout(() => {
        clearInterval(checkInterval);
    }, 5000);
}

function filterAndSortCards(searchTerm) {
    const cards = document.querySelectorAll('.calculator-card-wrapper');

    if (cards.length > 0) {
        const cardArray = Array.from(cards);

        cardArray.sort((a, b) => {
            const textA = a.querySelector('h3').textContent.toLowerCase();
            const textB = b.querySelector('h3').textContent.toLowerCase();
            return textA.localeCompare(textB);
        });

        cardArray.forEach((card) => {
            const searchText = card.getAttribute('data-name') || '';
            const cardTitle = card.querySelector('h3').textContent.toLowerCase();
            const cardDesc = card.querySelector('p').textContent.toLowerCase();
            const isMatch = searchText.includes(searchTerm) || 
                          cardTitle.includes(searchTerm) || 
                          cardDesc.includes(searchTerm);
            const sortedIndex = cardArray.indexOf(card);
            card.style.order = sortedIndex;
            card.style.display = isMatch ? 'block' : 'none';
        });
    }
}