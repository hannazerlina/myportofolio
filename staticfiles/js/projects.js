function openProjectModal() {
    const modal = document.getElementById("project-form-modal");
    if (modal && !modal.open) modal.showModal();
}

function closeProjectModal() {
    document.getElementById("project-form-modal")?.close();
}

// Shared by POST, PATCH and DELETE. A 204 deliberately has no JSON body.
async function writeProject(url, method, data) {
    const token = document.querySelector("#project-csrf input")?.value;
    const headers = { Accept: "application/json", "X-CSRFToken": token || "" };
    if (data !== undefined) headers["Content-Type"] = "application/json";
    const response = await fetch(url, {
        method, headers, credentials: "same-origin",
        ...(data !== undefined ? { body: JSON.stringify(data) } : {}),
    });
    if (response.status === 204) return null;
    const result = await response.json().catch(() => ({}));
    if (!response.ok) {
        const message = Object.entries(result).map(([field, errors]) => {
            const text = Array.isArray(errors) ? errors.join(" ") : String(errors);
            return field === "detail" ? text : `${field}: ${text}`;
        }).join(" ");
        throw new Error(message || `Permintaan gagal (${response.status}).`);
    }
    return result;
}

document.addEventListener("DOMContentLoaded", () => {
    const list = document.getElementById("project-list");
    if (!list) return;
    const searchForm = document.querySelector("[data-project-search-form]");
    const searchInput = document.querySelector("[data-project-search-input]");
    const query = () => searchInput?.value.trim() || "";
    const endpoint = (pattern, id) => pattern.replace("/0/", `/${id}/`);
    const notify = (title, message, type) => {
        if (typeof showToast === "function") showToast(title, message, type);
    };
    function element(tag, className, text) {
        const node = document.createElement(tag);
        node.className = className;
        if (text !== undefined) node.textContent = text;
        return node;
    }
    function buildProjectCard(project) {
        const card = element("article", "project-card");
        card.append(
            element("span", "project-status", `${project.role} · ${project.year}`),
            element("h2", "", project.title),
            element("p", "", project.description),
        );
        const actions = element("div", "project-card-actions");
        if (project.spotify_url) {
            try {
                const url = new URL(project.spotify_url);
                if (["http:", "https:"].includes(url.protocol)) {
                    const link = element("a", "social-link", "Dengarkan di Spotify ↗");
                    link.href = url.href;
                    link.target = "_blank";
                    link.rel = "noopener noreferrer";
                    actions.append(link);
                }
            } catch { /* Invalid legacy URLs should not prevent rendering the card. */ }
        }
        const starText = `${project.is_starred ? "★" : "☆"} Star (${project.star_count})`;
        if (list.dataset.isAuthenticated === "true") {
            const button = element("button", "social-link", starText);
            button.type = "button";
            button.dataset.action = "star";
            button.dataset.id = project.id;
            button.setAttribute("aria-pressed", String(project.is_starred));
            button.title = project.starred_by_names || "Belum ada star";
            actions.append(button);
        } else {
            const link = element("a", "social-link", starText);
            link.href = list.dataset.loginUrl;
            link.title = "Login untuk memberi star";
            actions.append(link);
        }
        if (list.dataset.isSuperuser === "true") {
            const button = element("button", "social-link", "Hapus");
            button.type = "button";
            button.dataset.action = "delete";
            button.dataset.id = project.id;
            button.dataset.title = project.title;
            actions.append(button);
        }
        card.append(actions);
        return card;
    }

    let activeRequest;
    async function fetchProjects() {
        activeRequest?.abort();
        const controller = new AbortController();
        activeRequest = controller;
        list.textContent = "Memuat proyek...";
        list.setAttribute("aria-busy", "true");
        try {
            const url = new URL(list.dataset.apiUrl, window.location.origin);
            url.searchParams.set("title", query());
            const response = await fetch(url, {
                headers: { Accept: "application/json" }, signal: controller.signal,
            });
            if (!response.ok) throw new Error(`Status ${response.status}`);
            const projects = await response.json();
            if (controller.signal.aborted) return;
            list.replaceChildren();
            if (!projects.length) {
                list.textContent = "Tidak ada proyek yang ditemukan.";
                return;
            }
            projects.forEach(project => list.append(buildProjectCard(project)));
        } catch (error) {
            if (error.name === "AbortError") return;
            list.textContent = "Gagal memuat proyek. Coba cari kembali.";
            notify("Gagal", "Tidak dapat memuat daftar proyek.", "error");
        } finally {
            if (activeRequest === controller) list.setAttribute("aria-busy", "false");
        }
    }

    list.addEventListener("click", async (event) => {
        const button = event.target.closest("button[data-action]");
        if (!button || button.disabled) return;
        const deleting = button.dataset.action === "delete";
        if (deleting && !confirm(`Hapus proyek "${button.dataset.title}"?`)) return;
        button.disabled = true;
        try {
            const result = await writeProject(
                endpoint(deleting ? list.dataset.detailUrl : list.dataset.starUrl, button.dataset.id),
                deleting ? "DELETE" : "POST",
            );
            notify("Berhasil", deleting ? "Proyek dihapus." :
                (result.is_starred ? "Star ditambahkan." : "Star dibatalkan."), "success");
            await fetchProjects();
        } catch (error) {
            notify("Gagal", error.message, "error");
        } finally {
            button.disabled = false;
        }
    });

    let searchTimer;
    searchInput?.addEventListener("input", () => {
        clearTimeout(searchTimer);
        searchTimer = setTimeout(fetchProjects, 300);
    });
    searchForm?.addEventListener("submit", event => {
        event.preventDefault();
        clearTimeout(searchTimer);
        fetchProjects();
    });

    const form = document.getElementById("project-form");
    form?.addEventListener("submit", async event => {
        event.preventDefault();
        const button = form.querySelector('[type="submit"]');
        const errorBox = document.getElementById("project-form-error");
        button.disabled = true;
        button.textContent = "Menyimpan...";
        errorBox.hidden = true;
        errorBox.textContent = "";
        try {
            const data = Object.fromEntries(new FormData(form));
            delete data.csrfmiddlewaretoken;
            await writeProject(form.action, "POST", data);
            form.reset();
            closeProjectModal();
            notify("Berhasil", "Proyek berhasil ditambahkan!", "success");
            await fetchProjects();
        } catch (error) {
            errorBox.textContent = error.message;
            errorBox.hidden = false;
            notify("Gagal", error.message, "error");
        } finally {
            button.disabled = false;
            button.textContent = "Simpan Proyek";
        }
    });
    fetchProjects();
});
