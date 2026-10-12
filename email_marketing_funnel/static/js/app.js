// Email Marketing Funnel – Frontend JS

document.addEventListener('DOMContentLoaded', () => {
    // Auto-hide flash messages after 4s
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(el => {
        setTimeout(() => {
            el.style.transition = 'opacity 0.4s';
            el.style.opacity = '0';
            setTimeout(() => el.remove(), 400);
        }, 4000);
    });

    // Confirm before destructive actions already handled via onclick

    // Optional: live stats refresh every 30s on dashboard
    if (document.getElementById('subs-chart')) {
        // Could poll /api/stats here if needed
    }
});
