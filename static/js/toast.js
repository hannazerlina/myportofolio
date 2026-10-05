let toastTimer;

function showToast(title, message, type = 'normal', duration = 3000) {
    const toast = document.getElementById('toast-component');
    const toastTitle = document.getElementById('toast-title');
    const toastMessage = document.getElementById('toast-message');

    if (!toast) return;

    toast.classList.remove(
        'toast-success',
        'toast-error',
        'toast-normal'
    );

    if (type === 'success') {
        toast.classList.add('toast-success');
    } else if (type === 'error') {
        toast.classList.add('toast-error');
    } else {
        toast.classList.add('toast-normal');
    }

    toastTitle.textContent = title;
    toastMessage.textContent = message;

    clearTimeout(toastTimer);

    if (!toast.matches(':popover-open')) {
        toast.showPopover();
        void toast.offsetHeight;
    }

    toast.classList.remove('toast-hidden');
    toast.classList.add('toast-show');

    toastTimer = setTimeout(() => {
        toast.classList.remove('toast-show');
        toast.classList.add('toast-hidden');

        toastTimer = setTimeout(() => {
            toast.hidePopover();
        }, 300);
    }, duration);
}