document.addEventListener('DOMContentLoaded', () => {
    const projectList = document.querySelector('[data-project-list]');
    const searchForm = document.querySelector('[data-project-search-form]');
    const searchInput = document.querySelector('[data-project-search-input]');

    if (!projectList || !searchForm || !searchInput) {
        return;
    }

    const apiUrl = projectList.dataset.apiUrl;

    const getCsrfToken = () => {
        const cookie = document.cookie
            .split('; ')
            .find((entry) => entry.startsWith('csrftoken='));

        return cookie ? decodeURIComponent(cookie.split('=')[1]) : '';
    };

    const escapeHtml = (value = '') => String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');

    const renderProjectCard = (project) => {
        const spotifyLink = project.spotify_url
            ? `<a class="social-link" href="${escapeHtml(project.spotify_url)}" target="_blank" rel="noopener noreferrer"><span>Dengarkan di Spotify ↗</span></a>`
            : '';

        return `
            <article class="project-card">
                <span class="project-status">${escapeHtml(project.role || 'Project')} · ${escapeHtml(project.year || '')}</span>
                <h2>${escapeHtml(project.title || 'Judul proyek')}</h2>
                <p>${escapeHtml(project.description || '')}</p>
                <div class="project-card-actions">
                    ${spotifyLink}
                    <div class="project-actions">
                        <button type="button" class="button button-danger" popovertarget="delete-project-${escapeHtml(project.id)}" aria-label="Hapus ${escapeHtml(project.title || 'proyek')}">
                            Hapus Proyek
                        </button>
                    </div>
                </div>
            </article>
        `;
    };

    const renderEmptyState = (query = '') => {
        const message = query
            ? 'Tidak ada proyek dengan nama tersebut.'
            : 'Belum ada proyek yang ditambahkan.';

        projectList.innerHTML = `
            <div class="empty-state">
                <p>${message}</p>
            </div>
        `;
    };

    const loadProjects = async (query = '') => {
        const queryParams = new URLSearchParams();
        if (query) {
            queryParams.set('title', query);
        }

        const requestUrl = queryParams.toString() ? `${apiUrl}?${queryParams.toString()}` : apiUrl;

        try {
            const response = await fetch(requestUrl, {
                headers: {
                    'Accept': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Request gagal');
            }

            const projects = await response.json();
            if (!Array.isArray(projects) || projects.length === 0) {
                renderEmptyState(query);
                return;
            }

            const cards = projects.map((project) => renderProjectCard(project.fields || project)).join('');
            projectList.innerHTML = cards;

            document.querySelectorAll('[data-delete-project-form]').forEach((deleteForm) => {
                deleteForm.addEventListener('submit', async (event) => {
                    event.preventDefault();
                    const form = event.currentTarget;
                    const submitButton = form.querySelector('button[type="submit"]');
                    const previousText = submitButton ? submitButton.textContent : 'Ya, Hapus';

                    if (submitButton) {
                        submitButton.disabled = true;
                        submitButton.textContent = 'Menghapus...';
                    }

                    try {
                        const response = await fetch(form.action, {
                            method: 'POST',
                            body: new FormData(form),
                            headers: {
                                'X-Requested-With': 'XMLHttpRequest',
                                'X-CSRFToken': getCsrfToken(),
                            },
                        });

                        if (!response.ok) {
                            throw new Error('Gagal menghapus proyek');
                        }

                        const modal = form.closest('[popover]');
                        if (modal && typeof modal.hide === 'function') {
                            modal.hide();
                        }

                        await loadProjects(searchInput.value.trim());
                    } catch (error) {
                        console.error('Error deleting project:', error);
                    } finally {
                        if (submitButton) {
                            submitButton.disabled = false;
                            submitButton.textContent = previousText;
                        }
                    }
                });
            });
        } catch (error) {
            console.error('Gagal memuat proyek:', error);
            renderEmptyState(query);
        }
    };

    searchForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const query = searchInput.value.trim();
        await loadProjects(query);
    });

    const initialQuery = searchInput.value.trim();
    loadProjects(initialQuery);
});
