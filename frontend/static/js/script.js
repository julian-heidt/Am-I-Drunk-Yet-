document.addEventListener('DOMContentLoaded', () => {
    const modeSwitch = document.getElementById('mode-switch');
    const themeSelector = document.getElementById('theme');
    const modeIcon = document.querySelector('label[for="mode-switch"] i');

    // --- Theme & Mode Management ---
    const applyMode = (mode) => {
        document.documentElement.setAttribute('data-bs-theme', mode);
        modeSwitch.checked = mode === 'dark';
        modeIcon.className = mode === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-stars-fill';
    };

    const applyTheme = (theme) => {
        document.documentElement.setAttribute('data-theme', theme);
    };

    // --- Event Listeners ---
    modeSwitch.addEventListener('change', function() {
        const mode = this.checked ? 'dark' : 'light';
        localStorage.setItem('mode', mode);
        applyMode(mode);
    });

    themeSelector.addEventListener('change', function() {
        const theme = this.value;
        localStorage.setItem('theme', theme);
        applyTheme(theme);
    });

    // --- Initialization ---
    const savedMode = localStorage.getItem('mode') || 'dark';
    const savedTheme = localStorage.getItem('theme') || 'default';

    applyMode(savedMode);
    themeSelector.value = savedTheme;
    applyTheme(savedTheme);
});
document.getElementById('bac-form').addEventListener('submit', function(event) {
    event.preventDefault();

    let weight = parseFloat(document.getElementById('weight').value);
    const weightUnit = document.getElementById('weight-unit').value;
    const gender = document.querySelector('input[name="gender"]:checked').value;
    const currentDrinks = parseInt(document.getElementById('current-drinks').value);

    // Convert weight to kg if necessary
    if (weightUnit === 'lbs') {
        weight = weight / 2.20462;
    }

    const data = {
        weight: weight,
        gender: gender,
        current_drinks: currentDrinks
    };

    const apiUrl = `http://backend:8080/api/calculate`;

    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        const drinksToTarget = document.getElementById('drinks-to-target');
        const timeToSober = document.getElementById('time-to-sober');

        if (data.error) {
            drinksToTarget.textContent = `Error: ${data.error}`;
            timeToSober.textContent = '';
        } else {
            if (data.drinks_to_reach_target > 0) {
                drinksToTarget.innerHTML = `<i class="bi bi-cup-straw"></i> You need to slam about <strong>${data.drinks_to_reach_target}</strong> more drinks to get legendary.`;
            } else {
                drinksToTarget.innerHTML = `<i class="bi bi-check-circle-fill"></i> Bro, you're already there. Send it!`;
            }

            if (data.time_to_sober > 0) {
                timeToSober.innerHTML = `<i class="bi bi-clock-history"></i> It'll take like <strong>${data.time_to_sober}</strong> hours 'til you're not seeing double.`;
            } else {
                timeToSober.innerHTML = `<i class="bi bi-emoji-sunglasses-fill"></i> You're sober, my dude. Time to change that.`;
            }
        }

        resultDiv.style.display = 'flex';
    })
    .catch(error => {
        console.error('Error:', error);
        const resultDiv = document.getElementById('result');
        const drinksToTarget = document.getElementById('drinks-to-target');
        drinksToTarget.textContent = 'An unexpected error occurred. Please try again.';
        resultDiv.style.display = 'block';
    });
});
