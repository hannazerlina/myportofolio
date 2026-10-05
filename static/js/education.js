function openEducationModal() {
    document.getElementById("education-modal")?.showModal();
}

function closeEducationModal() {
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

    function makePostForm(url, label, confirmation) {
        const form = document.createElement("form");
        form.method = "post";
        form.action = url;

        if (csrfInput) {
            form.append(csrfInput.cloneNode(true));
        }

        const button = makeElement("button", "social-link", label);
        button.type = "submit";
        form.append(button);

        if (confirmation) {
            form.addEventListener("submit", (event) => {
                if (!window.confirm(confirmation)) {
                    event.preventDefault();
                }
            });
        }

        return form;
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
            const starForm = makePostForm(
                itemUrl(list.dataset.starUrl, education.pk),
                `${education.is_starred ? "★" : "☆"} Star (${education.star_count})`
            );

            starForm.querySelector("button").setAttribute(
                "aria-pressed",
                String(education.is_starred)
            );

            actions.append(starForm);
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
            const edit = makeElement("a", "social-link", "Edit");
            edit.href = itemUrl(list.dataset.editUrl, education.pk);
            actions.append(edit);
        }

        if (superuser) {
            actions.append(makePostForm(
                itemUrl(list.dataset.deleteUrl, education.pk),
                "Hapus",
                "Yakin ingin menghapus pendidikan ini?"
            ));
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
            console.error(error);
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

    // Kode simpan modal akan kita tambahkan di sini.

    const educationForm = document.getElementById("education-form");

if (educationForm) {
    educationForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const button = educationForm.querySelector("[type='submit']");
        const errorBox = document.getElementById("education-form-error");

        button.disabled = true;
        button.textContent = "Menyimpan...";
        errorBox.hidden = true;
        errorBox.textContent = "";

        try {
            const response = await fetch(educationForm.action, {
                method: "POST",
                body: new FormData(educationForm),
            });

            const result = await response.json().catch(() => ({}));

            if (!response.ok) {
                const errors = Object.values(result.errors || {})
                    .flat()
                    .map((error) => error.message)
                    .join(" ");

                throw new Error(
                    errors || result.message || "Gagal menyimpan pendidikan."
                );
            }

            educationForm.reset();
            closeEducationModal();

            if (typeof showToast === "function") {
                showToast(
                    "Berhasil",
                    "Pendidikan berhasil ditambahkan!",
                    "success"
                );
            }

            await fetchEducation(searchInput.value.trim());
        } catch (error) {
            errorBox.textContent = error.message;
            errorBox.hidden = false;

            if (typeof showToast === "function") {
                showToast("Gagal", error.message, "error");
            }
        } finally {
            button.disabled = false;
            button.textContent = "Simpan Pendidikan";
        }
    });
}

    fetchEducation();
});