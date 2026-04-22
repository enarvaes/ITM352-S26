// main.js
// Small helpers used across the site. Most quiz logic lives in quiz.html.

document.addEventListener("DOMContentLoaded", function () {
    // Turn on Bootstrap tooltips if any elements opt in with data-bs-toggle.
    const tooltipTriggers = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggers.forEach(el => new bootstrap.Tooltip(el));
});

// Pop a dismissable alert at the top of the page.
function showNotification(message, type) {
    type = type || "success";
    const alertDiv = document.createElement("div");
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute("role", "alert");
    alertDiv.innerHTML = `${message}<button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;

    const container = document.querySelector(".container");
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        setTimeout(() => alertDiv.remove(), 5000);
    }
}
