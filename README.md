Nama : Hanna Zerlina Razaq Putri Wicaksono

NPM : 2506594692

Kelas : PBP E

Catatan Tugas 1: tidak menggunakan AI. Saya menyelesaikan tugas ini secara mandiri dengan mengatur ulang struktur halaman serta menyesuaikan konten profil dengan data diri sendiri. Prosesnya dilakukan dengan menguji tampilan langsung di halaman dan memastikan setiap elemen tetap rapi serta responsif.

### Tugas 1

1. Ya, saya menggunakan elemen semantik HTML5 seperti `section`, `article`, dan `aside` untuk membagi halaman portofolio menjadi bagian profil, detail informasi, dan konten tambahan. Elemen-elemen tersebut membuat struktur HTML lebih mudah dibaca, memudahkan styling dengan CSS, dan membantu menjaga halaman static tetap terorganisir tanpa kehilangan fokus pada isi.
2. Tantangan utama saat membuat layout responsif adalah menjaga keseimbangan antara foto, judul, dan deskripsi di layar yang sempit. Saya mengevaluasi elemen mana yang paling penting untuk dilihat pertama, lalu mengubah tata letak dari dua kolom menjadi satu kolom pada layar mobile agar informasi tetap jelas dan nyaman dibaca.
3. Batasan utama dari static web adalah keterbatasan untuk memperbarui data secara dinamis tanpa perlu mengubah file HTML atau CSS secara manual. Fungsionalitas yang paling ingin saya siapkan di iterasi berikutnya adalah fitur dinamis seperti daftar proyek yang dapat ditambah atau diubah dengan mudah, serta form kontak yang bisa mengirim data ke backend.

## Portofolio — Tugas 2

Portofolio Hanna Zerlina berbasis Django MVT. Halaman Education dan Projects menggunakan database, melanjutkan aplikasi `main` dari Tutorial 02. Profil menampilkan empat kelompok skills yang telah dikonfirmasi pemilik. Pengalaman Trinity diperbarui menjadi 2025–present dengan deskripsi persiapan debut.

### Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Windows: aktifkan virtual environment menggunakan `.venv\Scripts\activate`. Gunakan Python yang kompatibel dengan Django 5.2 dalam requirements. Buka http://127.0.0.1:8000/. Database lokal menggunakan SQLite. File `.env` dapat berisi `DEBUG=True` untuk debugging lokal; jangan commit `.env` atau database.

`0003_education_project.py` membuat tabel Education dan Project. `0004_portfolio_data.py` memasukkan pendidikan Labschool/UI, proyek Skylite Musicals 2024 beserta Spotify, dan memperbarui Trinity. Data awal disertakan lewat migrasi agar tersedia setelah setup baru, bukan ditulis di HTML. Migrasi data tidak menghapus data pribadi saat dibalik; rollback skema tetap menghapus tabel Education/Project. Experience memakai DateField lama: tanggal 1 Januari 2025 adalah penanda teknis untuk tahun yang diberikan pemilik, bukan klaim tanggal mulai sebenarnya. Template hanya menampilkan tahun. Dua pengalaman lama (Information Systems Student dan UI/UX Study Project) telah dihapus dari database lokal atas persetujuan pemilik.

### Struktur dan halaman

| URL | Named route | Template | Model |
| --- | --- | --- | --- |
| `/` | `main:show_main` | `index.html` | Experience |
| `/experience/` | `main:show_experience` | `experience.html` | Experience |
| `/education/` | `main:show_education` | `education.html` | Education |
| `/projects/` | `main:show_projects` | `projects.html` | Project |

Education: institution dan program (CharField), start_year dan end_year (PositiveSmallIntegerField; end_year opsional). Project: title dan role (CharField), year (PositiveSmallIntegerField), description (TextField), spotify_url (URLField opsional). Keduanya memiliki ID otomatis. View mengambil semua objek melalui ORM dan memasukkannya ke context; template menggunakan `for` dan `empty`. Semua halaman mewarisi navbar/footer dari `base.html`, dengan navigasi `{% url %}`. Scope terbatas pada daftar; tidak ada detail atau filter tambahan.

### Validasi

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Test mencakup URL/template, seluruh data, dan kondisi kosong untuk kedua halaman baru; juga experience/profil, navigasi bersama, HTML escaping, dan tautan Spotify opsional. Test memakai database terpisah dari data lokal.

### Tugas 2

1. Saat browser meminta `/education/`, `portofolio/urls.py` meneruskan pencocokan melalui `include('main.urls')`. `main/urls.py` mencocokkan `education/` dengan view `show_education` bernama `main:show_education`. View mengambil QuerySet `Education.objects.all()` dari model yang mendefinisikan struktur data di database. View memasukkan QuerySet ke context sebagai `education_list` lalu memanggil `render` dengan `education.html`. DTL mengulang objek dan menampilkan institusi, program, serta tahun; `empty` menampilkan pesan jika tidak ada data. Template mewarisi struktur `base.html`. Django mengembalikan HTML, kemudian browser memuat CSS dan menampilkan halaman. Alur Projects serupa melalui model Project dan context `project_list`.

2. Data di model dapat diperbarui tanpa menyunting struktur HTML, sehingga data dan tampilan punya tanggung jawab terpisah. Semua objek ditampilkan melalui satu perulangan; kita tidak perlu menyalin kartu HTML setiap menambah pendidikan atau proyek. Data yang sama bisa digunakan kembali untuk fitur lain. Tipe field juga menyatakan bentuk data, seperti angka tahun dan URL Spotify. Sebaliknya, data hard-coded lebih mudah tidak konsisten dan membuat pemeliharaan bercampur dengan perubahan desain. Validasi input tetap perlu diperhatikan: `save()` model tidak otomatis memanggil `full_clean()`.

3. `makemigrations` membandingkan model dengan state migrasi sebelumnya lalu menghasilkan file rencana perubahan skema; perintah ini belum mengubah tabel database. `migrate` menjalankan file migrasi sesuai dependensinya dan mencatat migrasi yang sudah diterapkan. Pada tugas ini, penambahan Education dan Project menghasilkan `0003_education_project.py`, lalu `migrate` membuat tabel keduanya. Jika nanti menambahkan field `description = models.TextField(blank=True)` ke Education, kedua perintah perlu dijalankan lagi. Mengedit nama institusi pada satu objek tidak memerlukan migrasi skema.

### AI disclosure dan log prompting

Tugas 2 dibantu OpenAI Codex untuk implementasi model/migrasi, view/URL, template/CSS, test, serta draf README dan jawaban reflektif. Pernyataan mandiri di bagian awal adalah catatan Tugas 1, bukan klaim untuk Tugas 2.

Ringkasan sesi: pengguna memberikan tautan tugas, meminta implementasi; percobaan awal terlalu luas lalu di-undo atas permintaan pengguna. Pengguna selanjutnya memilih Education dan Projects, memberikan CV dan koreksi pendidikan/pengalaman, tautan Spotify, serta mengonfirmasi skills Fasilkom. Codex menyampaikan daftar perubahan; pengguna menyetujui dengan “boleehh”. Implementasi ini mengikuti persetujuan tersebut. Tidak ada commit/push tanpa perintah pengguna. Ini ringkasan log, bukan transkrip lengkap. Jawaban reflektif merupakan draf berbantuan AI untuk dipelajari dan diperiksa pemilik sebelum pengumpulan.

### Pengumpulan

[Instruksi tugas](https://pbp.cs.ui.ac.id/assignments/individual/tugas-2.html) meminta tautan commit terakhir yang telah di-push, dengan repository publik. Format: `https://github.com/hannazerlina/myportofolio/commit/<SHA>`. Tenggat 14 September 2026, 23.59 WIB. Tutorial 02 adalah prasyarat dengan tenggat 9 September; status submisi perlu dicek di SCELE. Perubahan ini belum di-commit, di-push, atau di-deploy. Review hasil sebelum menyetujui commit.


### Pembaruan CV: Experience dan Achievements

Atas persetujuan pemilik, delapan pengalaman dari CV ditambahkan di samping Trinity (total sembilan). ByWonder dikoreksi menjadi Mei 2024 sampai tahun 2025. Semua rentang pengalaman ditampilkan sebagai tahun; tanggal pertama bulan menjadi representasi teknis ketika CV hanya menyebut bulan. Tanggal akhir ByWonder memakai 1 Januari 2025 sebagai penanda tahun, bukan klaim tanggal selesai sebenarnya. Sekar Watu Damar tercatat Desember 2024 sesuai CV. Angka capaian historis mengikuti CV, bukan statistik yang diperiksa secara langsung saat ini.

Halaman `/achievements/` memakai named route `main:show_achievements`, view `show_achievements`, dan template `achievements.html`. Model Achievement memiliki title, award, year, serta description, di luar ID otomatis. Empat pencapaian mencakup SkyPEX, South Jakarta Band Festival, National Indonesian Student Research Olympiad, serta Digital Poetry Musicalization Festival DKI Jakarta. Navbar bersama mencantumkan halaman baru; daftar memiliki kondisi kosong.

Migrasi `0005_achievement_alter_experience_category.py` menambah model dan pilihan kategori Organization/Event supaya pengalaman organisasi/acara tidak otomatis dilabeli pekerjaan part-time. Migrasi `0006_cv_experience_achievements.py` memasukkan data CV tanpa menimpa entri yang sudah ada dengan identitas sama. Jalankan `python manage.py migrate` di lingkungan lain. Pembalikan migrasi data mempertahankan data; pembalikan migrasi skema menghapus tabel Achievement.

Log AI lanjutan: pengguna meminta semua experience dan achievements dalam CV dimasukkan, menyetujui halaman Achievements tersendiri, dan mengoreksi akhir ByWonder menjadi 2025. Codex menambahkan model, migrasi, view, template, navbar, pengurutan pengalaman, dan test. Tidak ada commit/push dalam pembaruan ini.
