document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const nameInput = document.getElementById('name');
    const severityInput = document.getElementById('severity');
    const waitTimeInput = document.getElementById('wait_time');

    form.addEventListener('submit', function(event) {
        let valid = true;

        if (!nameInput.value) {
            alert('Name is required.');
            valid = false;
        }

        if (severityInput.value < 1 || severityInput.value > 10) {
            alert('Severity must be between 1 and 10.');
            valid = false;
        }

        if (waitTimeInput.value < 0) {
            alert('Wait time must be a positive number.');
            valid = false;
        }

        if (!valid) {
            event.preventDefault();
        }
    });
});
