(() => {
    const dialog = document.querySelector('.photo-viewer');
    const links = [...document.querySelectorAll('.moment-feature, .moment-photo')];
    if (!dialog || !links.length || typeof dialog.showModal !== 'function') return;
    const photo = dialog.querySelector('img');
    const stage = dialog.querySelector('.photo-viewer-stage');
    let current = 0;
    let previousOverflow = '';
    let touchStart = null;
    const show = (index) => {
        current = (index + links.length) % links.length;
        const source = links[current].querySelector('img');
        photo.src = links[current].href;
        photo.alt = source.alt;
        dialog.querySelector('#photo-caption').textContent = source.alt;
        dialog.querySelector('#photo-counter').textContent = `${current + 1} / ${links.length}`;
    };
    links.forEach((link, index) => link.addEventListener('click', (event) => {
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        show(index);
        previousOverflow = document.body.style.overflow;
        document.body.style.overflow = 'hidden';
        dialog.showModal();
    }));
    dialog.querySelector('.photo-viewer-close').addEventListener('click', () => dialog.close());
    dialog.querySelector('.photo-viewer-prev').addEventListener('click', () => show(current - 1));
    dialog.querySelector('.photo-viewer-next').addEventListener('click', () => show(current + 1));
    dialog.addEventListener('keydown', (event) => {
        if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
            event.preventDefault();
            show(current + (event.key === 'ArrowRight' ? 1 : -1));
        }
    });
    dialog.addEventListener('close', () => { document.body.style.overflow = previousOverflow; });
    stage.addEventListener('touchstart', (event) => {
        touchStart = event.touches.length === 1 ? [event.touches[0].clientX, event.touches[0].clientY] : null;
    }, { passive: true });
    stage.addEventListener('touchend', (event) => {
        if (!touchStart) return;
        const dx = event.changedTouches[0].clientX - touchStart[0];
        const dy = event.changedTouches[0].clientY - touchStart[1];
        if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) show(current + (dx < 0 ? 1 : -1));
        touchStart = null;
    }, { passive: true });
})();
