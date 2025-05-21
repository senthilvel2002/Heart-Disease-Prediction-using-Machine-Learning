// Function to switch between sections
function showSection(sectionId) {
    // Hide all sections
    const sectionsToHide = [
        'doctorForm',
        'trainingForm',
        'viewUserSection',
        'viewDoctorSection',
        'viewTrainingDataSection',
        'viewFeedbackSection'
    ];

    // Loop through all sections and hide them
    sectionsToHide.forEach(function(id) {
        const section = document.getElementById(id);
        if (section) {
            section.style.display = 'none';
        }
    });

    // Show selected section
    const activeSection = document.getElementById(sectionId);
    if (activeSection) {
        activeSection.style.display = 'block';
    } else {
        console.error('Section with ID "' + sectionId + '" not found!');
    }
}

// Show default section on page load
window.onload = function () {
    // Get the 'open_section' value passed by Flask, ensuring it is properly passed as a string
    var openSection = "{{ open_section | tojson | safe }}";

    if (openSection && openSection !== "null") {
        // If 'open_section' is set and not null, auto-show that section
        showSection(openSection);
    } else {
        // Default to 'doctorForm' if no section is specified
        showSection('doctorForm');
    }
};
