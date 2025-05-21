document.addEventListener("DOMContentLoaded", function() {
    // Here you can add any additional interactivity if needed.
    // For example, you can add custom sorting or filter functionality to the table.
    
    const tableRows = document.querySelectorAll('.user-table tr');
    
    // Example: You can highlight a row on hover
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            row.style.backgroundColor = '#f1f1f1';
        });
        
        row.addEventListener('mouseleave', function() {
            row.style.backgroundColor = '';
        });
    });
});
