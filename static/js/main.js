// Main JavaScript for interactive features

// Auto-hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function () {
    const flashMessages = document.querySelectorAll('.flash');

    flashMessages.forEach(function (flash) {
        setTimeout(function () {
            flash.style.opacity = '0';
            flash.style.transition = 'opacity 0.3s';
            setTimeout(function () {
                flash.remove();
            }, 300);
        }, 5000);
    });
});
