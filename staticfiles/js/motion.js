(() => {
    const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (preference.matches || !('IntersectionObserver' in window) || !Element.prototype.animate) return;

    const running = new Set();
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(({ target, isIntersecting }) => {
            if (!isIntersecting) return;
            observer.unobserve(target);
            if (preference.matches) return;
            const animation = target.animate(
                [{ opacity: 0, transform: 'translateY(16px)' }, { opacity: 1, transform: 'translateY(0)' }],
                { duration: 520, easing: 'cubic-bezier(0.2, 0.65, 0.3, 1)' }
            );
            running.add(animation);
            animation.onfinish = () => running.delete(animation);
        });
    }, { threshold: 0.08 });

    document.querySelectorAll('.hero-grid, .skill-card, .experience-card, .project-card').forEach((card) => observer.observe(card));
    preference.addEventListener('change', (event) => {
        if (!event.matches) return;
        observer.disconnect();
        running.forEach((animation) => animation.cancel());
        running.clear();
    });
})();
