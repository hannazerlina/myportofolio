document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('[data-project-form]');
    if (!form) return;

    const errorBox = document.querySelector('[data-project-form-errors]');

    const getCsrfToken = () => {
        const cookie = document.cookie
            .split('; ')
            .find((entry) => entry.startsWith('csrftoken='));

        return cookie ? decodeURIComponent(cookie.split('=')[1]) : '';
    };

    const clearFieldErrors = () => {
        document.querySelectorAll('.editor-field-invalid, .editor-field-errors').forEach((node) => {
            node.classList.remove('editor-field-invalid');
            if (node.classList.contains('editor-field-errors')) {
                node.innerHTML = '';
            }
        });
    };

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton ? submitButton.textContent : 'Simpan';

        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = 'Menyimpan...';
        }

        clearFieldErrors();

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCsrfToken(),
                },
            });

            const data = await response.json().catch(() => null);

            if (!response.ok) {
                const errors = data && data.errors ? data.errors : {};
                const generalErrors = Object.values(errors).flat();

                if (errorBox) {
                    errorBox.innerHTML = generalErrors.length
                        ? `<ul>${generalErrors.map((message) => `<li>${message}</li>`).join('')}</ul>`
                        : '<p>Terjadi kesalahan saat menyimpan proyek.</p>';
                    errorBox.hidden = false;
                }

                return;
            }

            if (data && data.redirect_url) {
                window.location.href = data.redirect_url;
                return;
            }

            window.location.href = form.dataset.redirectUrl || '/projects/';
        } catch (error) {
            console.error('Error submitting project:', error);
            if (errorBox) {
                errorBox.innerHTML = '<p>Gagal mengirim data. Coba lagi.</p>';
                errorBox.hidden = false;
            }
        } finally {
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = originalText;
            }
        }
    });
});
