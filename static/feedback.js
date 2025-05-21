document.getElementById('feedbackForm').addEventListener('submit', function (event) {
    const email = document.getElementById('user_email').value.trim();
    const feedback = document.getElementById('feedback_text').value.trim();

    if (!email || !feedback) {
        alert("Please fill in both fields.");
        event.preventDefault();
    } else {
        document.getElementById('feedback-message').textContent = "✅ Thank you for your feedback!";
    }
});
