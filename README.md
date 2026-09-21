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

## Portofolio — Tutor 3

Pada tutor 3, saya menambahkan fitur form dan data delivery untuk project. Saya membuat model form agar user dapat menambahkan project baru melalui halaman form, lalu data dikirim ke backend menggunakan request POST dan disimpan ke database.

Saya juga menambahkan endpoint JSON untuk mengambil data project dari server serta fitur pencarian berdasarkan judul project. Selain itu, saya menambahkan fitur hapus project dengan modal konfirmasi agar proses pengelolaan project lebih mudah dan rapi.

### Fitur yang ditambahkan

- Form tambah project
- Validasi input form
- JSON API untuk project
- Search project berdasarkan judul
- Hapus project dengan konfirmasi
- Integrasi antara template, view, dan frontend JavaScript

### Pengujian

```bash
python manage.py test
```

Semua pengujian berhasil dijalankan dan project tetap dalam kondisi aman.

### Tugas 3

1. ModelForm membantu membuat form berdasarkan model Django. Pada proyek ini, EducationForm menggunakan field institution, program, start_year, dan end_year dari model Education. ModelForm menyediakan validasi serta penyimpanan data, sehingga tidak semuanya perlu ditulis manual. Saat edit, instance=education membuat form memperbarui objek yang dipilih.
   
{% csrf_token %} diperlukan pada form POST untuk membantu Django menolak permintaan palsu dari situs lain yang memanfaatkan browser pengguna. Token ini bukan pengganti autentikasi atau izin akses.

2. JSON sering dipilih karena sintaksnya ringkas dan mudah diolah dengan JavaScript maupun bahasa lain. JSON mendukung objek, array, string, angka, boolean, dan null. XML menggunakan tag pembuka dan penutup sehingga biasanya lebih panjang. Meskipun demikian, XML tetap berguna pada sistem yang membutuhkan struktur dokumen atau fitur khusus XML.

3. Ketika /api/education/ dibuka, urls.py mengarahkan      request ke get_education_json. View mengambil data menggunakan Education.objects.all(), kemudian serializers.serialize mengubahnya menjadi teks JSON. HttpResponse mengirim hasilnyadengan content type application/json.
   
Serialization diperlukan karena objek model Django tidak dapat langsung dikirim sebagai JSON. Pada halaman Education, show_education membaca respons JSON, melakukan deserialization, lalu meneruskan objek Education ke template melalui context.

### AI disclosure

Saya menggunakan ChatGPT sebagai pendamping belajar untuk memahami ModelForm, GET/POST, CSRF, serta serialization dan deserialization JSON. Bantuan diberikan melalui penjelasan bertahap, contoh kode, dan pemeriksaan implementasi. Saya memasukkan kode EducationForm, view tambah/edit/hapus, routing, dan template secara bertahap, lalu mencoba alurnya menggunakan data latihan. 

### Bagian spesifik yang dibantu AI

Pada pengerjaan Tugas 3, AI membantu:
- Menjelaskan ModelForm, labels, widgets, GET/POST, CSRF,
  primary key, serialization, dan deserialization.
- Memberikan contoh kode EducationForm serta view tambah,
  edit, hapus, dan penyedia data JSON.
- Memberikan contoh routing dan template form Education.
- Menjelaskan penggunaan instance pada form edit agar
  penyimpanan memperbarui objek yang dipilih.
- Memeriksa potongan kode, termasuk indentasi fungsi dan
  form Hapus yang keliru ditempatkan di dalam tautan Edit.
- Memeriksa file yang tersimpan dan menjalankan pemeriksaan
  Django.