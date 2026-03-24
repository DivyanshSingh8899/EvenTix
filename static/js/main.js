/* static/js/main.js */
document.addEventListener('DOMContentLoaded', () => {
    // Add micro-animations by observing elements as they scroll into view
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    const cards = document.querySelectorAll('.glass-card');
    cards.forEach((card, index) => {
        // Stagger the animation
        card.style.opacity = '0';
        card.style.animationDelay = `${index * 0.1}s`;
        observer.observe(card);
    });
});
