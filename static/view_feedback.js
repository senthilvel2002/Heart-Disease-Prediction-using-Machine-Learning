// JavaScript for smooth hover effects on rows and back button functionality
document.addEventListener('DOMContentLoaded', function() {
    const rows = document.querySelectorAll('tbody tr');
    rows.forEach(row => {
        row.addEventListener('mouseover', () => {
            row.style.cursor = 'pointer';
        });
        row.addEventListener('mouseout', () => {
            row.style.cursor = 'default';
        });
    });

    // Back button behavior
    const backButton = document.querySelector('.back-btn');
    backButton.addEventListener('click', function() {
        window.history.back();
    });
});
