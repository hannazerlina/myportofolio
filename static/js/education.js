function openEducationModal(education = null) {
    const modal = document.getElementById("education-modal");
    const form = document.getElementById("education-form");
    if (!modal || !form || form.dataset.saving === "true") return;
    form.reset();
    form.dataset.editId = education ? String(education.id) : "";
    document.getElementById("education-modal-title").textContent =
        education ? "Edit Pendidikan" : "Tambah Pendidikan";
    const errorBox = document.getElementById("education-form-error");
    errorBox.hidden = true;
    errorBox.textContent = "";
    if (education) {
        for (const name of ["institution", "program", "start_year", "end_year"]) {
            form.elements.namedItem(name).value = education[name] ?? "";
        }
    }
    if (!modal.open) modal.showModal();
}

function closeEducationModal() {
    if (document.getElementById("education-form")?.dataset.saving === "true") return;
    document.getElementById("education-modal")?.close();
}

document.addEventListener("DOMContentLoaded", () => {
    const list = document.getElementById("education-list");
    if (!list) return;

    const searchForm = document.getElementById("education-search");
    const searchInput = document.getElementById("education-search-input");
    const csrfInput = document.querySelector(
        "#education-csrf input[name='csrfmiddlewaretoken']"
    );

    const authenticated = list.dataset.isAuthenticated === "true";
    const superuser = list.dataset.isSuperuser === "true";
    const editor = list.dataset.isEditor === "true";

    function makeElement(tag, className, text) {
        const element = document.createElement(tag);
        element.className = className;
        if (text !== undefined) element.textContent = text;
        return element;
    }

    function itemUrl(pattern, id) {
        return pattern.replace("/0/", `/${id}/`);
    }

    function notify(title, message, type) {
        if (typeof showToast === "function") showToast(title, message, type);
    }

    async function requestEducation(url, method = "GET", data) {
        const headers = { Accept: "application/json" };
        if (method !== "GET") headers["X-CSRFToken"] = csrfInput?.value || "";
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

    function actionButton(action, education, label) {
        const button = makeElement("button", "social-link", label);
        button.type = "button";
        button.dataset.action = action;
        button.dataset.id = education.id;
        button.dataset.institution = education.institution;
        return button;
    }

    function makeCard(education) {
        const card = makeElement("article", "experience-card");
        const years = makeElement(
            "span",
            "experience-year",
            `${education.start_year} — ${education.end_year ?? "Present"}`
        );

        const institution = makeElement("div", "education-institution");
        let logoUrl = "";

        if (education.institution.includes("Labschool")) {
            logoUrl = list.dataset.labschoolLogo;
        } else if (education.institution.includes("Indonesia")) {
            logoUrl = list.dataset.uiLogo;
        }

        if (logoUrl) {
            const logo = document.createElement("img");
            logo.src = logoUrl;
            logo.alt = `Logo ${education.institution}`;
            institution.append(logo);
        }

        institution.append(makeElement("h2", "", education.institution));

        const program = makeElement("p", "", education.program);
        const actions = makeElement("div", "project-card-actions");

        if (authenticated) {
            const starButton = actionButton("star", education,
                `${education.is_starred ? "★" : "☆"} Star (${education.star_count})`);
            starButton.setAttribute("aria-pressed", String(education.is_starred));
            actions.append(starButton);
        } else {
            actions.append(
                makeElement("span", "", `☆ ${education.star_count} star`)
            );

            const login = makeElement(
                "a", "social-link", "Login untuk memberi star"
            );
            login.href = list.dataset.loginUrl;
            actions.append(login);
        }

        if (superuser || editor) {
            actions.append(actionButton("edit", education, "Edit"));
        }
        if (superuser) {
            actions.append(actionButton("delete", education, "Hapus"));
        }

        card.append(years, institution, program, actions);
        return card;
    }

    let activeRequest;

    async function fetchEducation(query = "") {
        activeRequest?.abort();
        const controller = new AbortController();
        activeRequest = controller;

        list.textContent = "Memuat pendidikan...";
        list.setAttribute("aria-busy", "true");

        try {
            const url = new URL(list.dataset.apiUrl, window.location.origin);
            url.searchParams.set("institution", query);

            const response = await fetch(url, {
                signal: controller.signal,
                headers: { Accept: "application/json" },
            });

            if (!response.ok) {
                throw new Error("Gagal mengambil data pendidikan.");
            }

            const data = await response.json();
            if (controller.signal.aborted) return;

            list.replaceChildren();

            if (data.length === 0) {
                list.append(makeElement(
                    "p",
                    "empty-state",
                    query
                        ? "Tidak ada institusi yang cocok."
                        : "Belum ada pendidikan yang ditambahkan."
                ));
                return;
            }

            data.forEach((education) => {
                list.append(makeCard(education));
            });
        } catch (error) {
            if (error.name === "AbortError") return;

            list.textContent = "Gagal memuat pendidikan. Coba cari kembali.";
            notify("Gagal", "Tidak dapat memuat pendidikan.", "error");
        } finally {
            if (activeRequest === controller) {
                list.setAttribute("aria-busy", "false");
            }
        }
    }

    let searchTimer;

    searchInput.addEventListener("input", () => {
        clearTimeout(searchTimer);
        searchTimer = setTimeout(() => {
            fetchEducation(searchInput.value.trim());
        }, 300);
    });

    searchForm.addEventListener("submit", (event) => {
        event.preventDefault();
        clearTimeout(searchTimer);
        fetchEducation(searchInput.value.trim());
    });

    list.addEventListener("click", async (event) => {
        const button = event.target.closest("button[data-action]");
        if (!button || button.disabled) return;
        const action = button.dataset.action;
        const detailUrl = itemUrl(list.dataset.detailUrl, button.dataset.id);
        if (action === "delete" && !confirm(`Hapus pendidikan "${button.dataset.institution}"?`)) return;
        button.disabled = true;
        try {
            if (action === "edit") {
                const education = await requestEducation(detailUrl);
                openEducationModal(education);
                return;
            }
            const result = await requestEducation(
                action === "star" ? itemUrl(list.dataset.starUrl, button.dataset.id) : detailUrl,
                action === "star" ? "POST" : "DELETE",
            );
            notify("Berhasil", action === "delete" ? "Pendidikan dihapus." :
                (result.is_starred ? "Star ditambahkan." : "Star dibatalkan."), "success");
            await fetchEducation(searchInput.value.trim());
        } catch (error) {
            notify("Gagal", error.message, "error");
        } finally {
            button.disabled = false;
        }
    });

    const educationForm = document.getElementById("education-form");
    const modal = document.getElementById("education-modal");
    modal?.addEventListener("cancel", (event) => {
        if (educationForm.dataset.saving === "true") event.preventDefault();
    });
    educationForm?.addEventListener("submit", async (event) => {
        event.preventDefault();
        if (educationForm.dataset.saving === "true") return;
        const button = educationForm.querySelector("[type='submit']");
        const errorBox = document.getElementById("education-form-error");
        const editId = educationForm.dataset.editId;
        educationForm.dataset.saving = "true";
        button.disabled = true;
        button.textContent = "Menyimpan...";
        errorBox.hidden = true;
        errorBox.textContent = "";
        try {
            const data = Object.fromEntries(new FormData(educationForm));
            delete data.csrfmiddlewaretoken;
            // An empty optional year is JSON null, not an invalid integer string.
            data.end_year = data.end_year === "" ? null : Number(data.end_year);
            data.start_year = Number(data.start_year);
            await requestEducation(
                editId ? itemUrl(list.dataset.detailUrl, editId) : educationForm.action,
                editId ? "PATCH" : "POST", data,
            );
            educationForm.dataset.saving = "false";
            closeEducationModal();
            educationForm.reset();
            notify("Berhasil", editId ? "Pendidikan diperbarui!" : "Pendidikan ditambahkan!", "success");
            await fetchEducation(searchInput.value.trim());
        } catch (error) {
            errorBox.textContent = error.message;
            errorBox.hidden = false;
            notify("Gagal", error.message, "error");
        } finally {
            educationForm.dataset.saving = "false";
            button.disabled = false;
            button.textContent = "Simpan Pendidikan";
        }
    });

    fetchEducation();
});
