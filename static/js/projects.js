function openProjectModal() {
    const modal = document.getElementById("project-form-modal");
    if (modal && !modal.open) {
        modal.showModal();
    }
}

function closeProjectModal() {
    const modal = document.getElementById("project-form-modal");
    if (modal) {
        modal.close();
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const projectList = document.getElementById("project-list");
    if (!projectList) return;

    const searchForm = document.querySelector("[data-project-search-form]");
    const searchInput = document.querySelector("[data-project-search-input]");

    function buildProjectCard(project) {
        const card = document.createElement("article");
        card.className = "project-card";

        const status = document.createElement("span");
        status.className = "project-status";
        status.textContent = `${project.role} · ${project.year}`;

        const title = document.createElement("h2");
        title.textContent = project.title;

        const description = document.createElement("p");
        description.textContent = project.description;

        card.append(status, title, description);

        if (project.spotify_url) {
            const url = new URL(project.spotify_url, window.location.origin);

            if (["https:", "http:"].includes(url.protocol)) {
                const link = document.createElement("a");
                link.className = "social-link";
                link.href = url.href;
                link.target = "_blank";
                link.rel = "noopener noreferrer";
                link.textContent = "Dengarkan di Spotify ↗";
                card.append(link);
            }
        }
        
        const starForm = document.createElement("form");
        starForm.method = "post";
        starForm.action = `/projects/${project.pk}/star/`;

        if (projectList.dataset.isAuthenticated === "true") {
            const csrf = document.querySelector(
                "#project-csrf input"
            ).cloneNode(true);
            starForm.append(csrf);

            const starButton = document.createElement("button");
            starButton.type = "submit";
            starButton.className = "social-link";
            starButton.textContent =
                `${project.is_starred ? "★" : "☆"} Star (${project.star_count})`;
            starButton.setAttribute(
                "aria-pressed",
                String(project.is_starred)
            );

            starForm.append(starButton);
            card.append(starForm);
        } else {
            const loginLink = document.createElement("a");
            loginLink.href = projectList.dataset.loginUrl;
            loginLink.className = "social-link";
            loginLink.textContent = `☆ Star (${project.star_count})`;
            card.append(loginLink);
        }

                if (projectList.dataset.isSuperuser === "true") {
            const deleteButton = document.createElement("button");
            deleteButton.type = "button";
            deleteButton.className = "social-link";
            deleteButton.textContent = "Hapus";

            deleteButton.addEventListener("click", async () => {
                if (!confirm(`Hapus proyek "${project.title}"?`)) return;

                deleteButton.disabled = true;

                try {
                    const csrf = document.querySelector(
                        "#project-csrf input"
                    ).value;

                    const response = await fetch(
                        `/projects/${project.pk}/delete/`,
                        {
                            method: "POST",
                            headers: {
                                "X-CSRFToken": csrf,
                                "X-Requested-With": "XMLHttpRequest",
                            },
                        }
                    );

                    const result = await response.json().catch(() => ({}));

                    if (!response.ok || !result.success) {
                        throw new Error("Penghapusan ditolak.");
                    }

                    showToast("Berhasil", "Proyek dihapus.", "success");
                    await fetchProjects(
                        searchInput ? searchInput.value.trim() : ""
                    );
                } catch (error) {
                    showToast(
                        "Gagal",
                        "Proyek belum bisa dihapus. Coba lagi.",
                        "error"
                    );
                    console.error(error);
                } finally {
                    deleteButton.disabled = false;
                }
            });

            card.append(deleteButton);
        }
        return card;
    }

    async function fetchProjects(query = "") {
        projectList.textContent = "Memuat proyek...";

        const url = new URL(
            projectList.dataset.apiUrl,
            window.location.origin
        );
        url.searchParams.set("title", query);

        try {
            const response = await fetch(url);

            if (!response.ok) {
                throw new Error(`Status ${response.status}`);
            }

            const projects = await response.json();
            projectList.replaceChildren();

            if (projects.length === 0) {
                projectList.textContent = "Tidak ada proyek yang ditemukan.";
                return;
            }

            projects.forEach((project) => {
                projectList.append(buildProjectCard(project));
            });
        } catch (error) {
            projectList.textContent = "Gagal memuat proyek. Coba lagi.";
            showToast("Gagal", "Tidak dapat memuat daftar proyek.", "error");
            console.error(error);
        }
    }

    if (searchForm && searchInput) {
        let searchTimer;

        searchInput.addEventListener("input", () => {
            clearTimeout(searchTimer);

            searchTimer = setTimeout(() => {
                fetchProjects(searchInput.value.trim());
            }, 300);
        });

        searchForm.addEventListener("submit", (event) => {
            event.preventDefault();
            clearTimeout(searchTimer);
            fetchProjects(searchInput.value.trim());
        });
    }
    
    const projectForm = document.getElementById("project-form");

    if (projectForm) {
        projectForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const button = projectForm.querySelector('[type="submit"]');
            button.disabled = true;
            button.textContent = "Menyimpan...";

            try {
                const response = await fetch(projectForm.action, {
                    method: "POST",
                    body: new FormData(projectForm),
                });

                const result = await response.json().catch(() => ({}));

                if (!response.ok) {
                    const errors = result.errors
                        ? Object.values(result.errors)
                            .flat()
                            .map((error) => error.message)
                            .join(" ")
                        : result.message || `Gagal menyimpan (${response.status}).`;

                    showToast("Gagal", errors, "error");
                    return;
                }

                projectForm.reset();
                closeProjectModal();
                showToast("Berhasil", "Proyek berhasil ditambahkan!", "success");
                await fetchProjects(searchInput ? searchInput.value.trim() : "");
            } catch (error) {
                showToast(
                    "Gagal",
                    "Tidak dapat terhubung ke server. Coba lagi.",
                    "error"
                );
                console.error(error);
            } finally {
                button.disabled = false;
                button.textContent = "Simpan Proyek";
            }
        });
    }
    fetchProjects(searchInput ? searchInput.value.trim() : "");
});