Nama : Hanna Zerlina Razaq Putri Wicaksono

NPM : 2506594692

Kelas : PBP E

Catatan Tugas 1: tidak menggunakan AI. Saya menyelesaikan tugas ini secara mandiri dengan mengatur ulang struktur halaman serta menyesuaikan konten profil dengan data diri sendiri. Prosesnya dilakukan dengan menguji tampilan langsung di halaman dan memastikan setiap elemen tetap rapi serta responsif.

### Tugas 1

1. Ya, saya menggunakan elemen semantik HTML5 seperti `section`, `article`, dan `aside` untuk membagi halaman portofolio menjadi bagian profil, detail informasi, dan konten tambahan. Elemen-elemen tersebut membuat struktur HTML lebih mudah dibaca, memudahkan styling dengan CSS, dan membantu menjaga halaman static tetap terorganisir tanpa kehilangan fokus pada isi.
2. Tantangan utama saat membuat layout responsif adalah menjaga keseimbangan antara foto, judul, dan deskripsi di layar yang sempit. Saya mengevaluasi elemen mana yang paling penting untuk dilihat pertama, lalu mengubah tata letak dari dua kolom menjadi satu kolom pada layar mobile agar informasi tetap jelas dan nyaman dibaca.
3. Batasan utama dari static web adalah keterbatasan untuk memperbarui data secara dinamis tanpa perlu mengubah file HTML atau CSS secara manual. Fungsionalitas yang paling ingin saya siapkan di iterasi berikutnya adalah fitur dinamis seperti daftar proyek yang dapat ditambah atau diubah dengan mudah, serta form kontak yang bisa mengirim data ke backend.

## Portofolio — Tugas 2

Portofolio Hanna Zerlina berbasis Django MVT. Pada tugas ini saya menambahkan halaman Education dan Projects yang mengambil data dari database.

### Perubahan Tugas 2

- Menambahkan model `Education` dan `Project`, masing-masing dengan beberapa field selain primary key.
- Menambahkan migrasi untuk membuat tabel dan mengisi data awal.
- Membuat view dan template baru untuk halaman Education dan Projects.
- Menambahkan named route dan tautan halaman baru pada navbar.
- Menampilkan seluruh data dengan perulangan Django Template Language.
- Menambahkan tampilan kondisi kosong jika belum ada data.
- Menambahkan unit test untuk URL, template, data, dan kondisi kosong.
- Menambahkan halaman Achievements sebagai pengembangan tambahan.
- Menambahkan logo UI dan SMA Labschool pada halaman Education.

### Jawaban Pertanyaan Tugas 2

1. Saat membuka halaman Education, request diterima oleh `portofolio/urls.py`, lalu diteruskan ke `main/urls.py`. URL tersebut menjalankan view `show_education`. View mengambil data dari model `Education`, memasukkannya ke context, lalu mengirimkannya ke template `education.html`. Template menampilkan data tersebut di browser.

2. Data disimpan di model supaya dapat diubah atau ditambah tanpa mengubah HTML. Dengan begitu, kode lebih mudah dirawat dan data dapat ditampilkan menggunakan perulangan.

3. `makemigrations` digunakan untuk membuat file migrasi berdasarkan perubahan model. `migrate` digunakan untuk menerapkan migrasi tersebut ke database. Contohnya, ketika menambahkan model `Education`, saya menjalankan kedua perintah tersebut agar tabelnya dibuat di database.

### Cara Menjalankan

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Buka `http://127.0.0.1:8000/` pada browser.

### Pengujian

```bash
python manage.py test
```

Hasil pengujian: 19 test berhasil.

### AI Disclosure

Saya menggunakan bantuan ChatGPT sebagai bantuan dalam mengembangkan model, migrasi, view, URL, template, CSS, dan unit test untuk Tugas 2. Saya tetap memeriksa dan menjalankan pengujian pada proyek.
