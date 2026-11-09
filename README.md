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


### Tugas 4

Pada tugas ini, saya melanjutkan fitur Education dari Tugas 3
dengan menerapkan autentikasi, pembatasan hak akses, dan star.

#### Hak akses

- Pengunjung dapat melihat data pendidikan tanpa login.
- Pengguna yang sudah login dapat memberi atau membatalkan star.
- Anggota grup Editor dapat mengedit pendidikan, tetapi tidak
  dapat menambah atau menghapusnya.
- Superuser dapat menambah, mengedit, dan menghapus pendidikan.

Grup Editor dan keanggotaannya diatur melalui Django Admin.
Pembatasan diterapkan pada view serta tampilan tombol di template.

#### Fitur star

Education memiliki relasi ManyToManyField dengan User.
Setiap pengguna dapat memberi maksimal satu star per pendidikan
dan membatalkannya. Aksi star menggunakan POST dan CSRF token.

Endpoint `/api/education/` menyediakan data pendidikan dalam
format JSON, dengan username sebagai penanda pemberi star.

#### AI Disclosure

Saya menggunakan ChatGPT sebagai pendamping
belajar untuk memahami autentikasi, hak akses, dan fitur star
pada Django.

Saya meminta penjelasan bertahap, contoh kode, serta bantuan
memeriksa potongan kode dan pesan error.

Bantuan AI meliputi:
- Menjelaskan perbedaan hak akses pengguna biasa, Editor,
  dan superuser.
- Memberikan panduan pembuatan grup Editor melalui Django Admin.
- Membimbing implementasi relasi ManyToManyField, fungsi star,
  routing, dan komponen tombol star Education.
- Membantu menemukan penyebab error NoReverseMatch akibat
  tombol Edit berada di luar perulangan template.
- Menjelaskan CSS untuk warna, ukuran, dan ketebalan tulisan.

Contoh interaksi selama pengerjaan:
- “star itu utk apa?” untuk memahami fungsi star.
- “font weight utk ap” untuk memahami ketebalan tulisan.

Saya mempelajari dan mencoba hasilnya melalui browser, termasuk
akses Editor dan fitur star. 

### Tutorial 5 — Web Interactivity with JavaScript

Pada tutorial ini, saya mengembangkan halaman Projects dengan:
- Memuat daftar proyek melalui Fetch API.
- Menerapkan pencarian dengan debounce 300 milidetik.
- Menampilkan form tambah proyek dalam modal.
- Menambah dan menghapus proyek melalui AJAX tanpa reload.
- Menampilkan notifikasi berhasil atau gagal menggunakan toast.
- Memvalidasi input melalui ProjectForm dan method clean.
- Menggunakan textContent agar data ditampilkan sebagai teks, bukan dieksekusi sebagai HTML.

Aksi tambah dan hapus tetap dibatasi untuk superuser di server.
Permintaan POST menyertakan token CSRF.

#### Pengujian

Saya mencoba pencarian, membuka dan menutup modal, menambahkan
proyek, menolak judul yang hanya berisi tag HTML, serta menghapus
proyek percobaan melalui AJAX.

#### AI Disclosure
Saya menggunakan ChatGPT untuk penjelasan bertahap,
contoh kode, dan debugging. Bantuan mencakup penjelasan toast, Fetch API, debounce, modal, validasi, serta penelusuran masalah CSRF dan file statis.

### Tugas 5

 1. Apa itu debouncing dan mengapa penting untuk pencarian AJAX?

Debouncing adalah teknik menunda pemanggilan fungsi sampai pengguna
berhenti melakukan suatu aktivitas selama waktu tertentu.

Pada pencarian Education, saya menggunakan jeda 300 milidetik.
Setiap pengguna mengetik kembali, timer sebelumnya dibatalkan.
Dengan begitu, permintaan pencarian tidak dikirim untuk setiap
huruf yang diketik, sehingga mengurangi permintaan ke server.

2. Mengapa menggunakan await pada fetch? Apa yang terjadi tanpa await?

fetch() mengembalikan Promise. await menunggu Promise tersebut
selesai sebelum melanjutkan baris berikutnya dalam fungsi async,
tanpa menghentikan seluruh interaksi halaman.

Tanpa await, variabel hasil fetch() masih berupa Promise, bukan
objek Response. Kita perlu menangani hasilnya menggunakan .then()
atau menunggunya dengan await sebelum membaca respons.

response.json() juga mengembalikan Promise, sehingga perlu
ditunggu untuk mendapatkan data JSON yang sudah diubah menjadi
objek JavaScript.

3. Apa itu XSS dan mengapa rendering melalui JavaScript perlu diperhatikan?

Cross-Site Scripting (XSS) adalah serangan ketika input yang tidak
tepercaya diperlakukan sebagai kode aktif dan dijalankan oleh browser.

Django template melakukan autoescaping secara default. Saat membuat
tampilan melalui JavaScript, perlindungan itu tidak otomatis berlaku.
Memasukkan data tidak tepercaya ke innerHTML dapat membuat browser
menafsirkannya sebagai HTML dan membuka celah XSS.

Pada Education, saya menggunakan textContent untuk menampilkan
data sebagai teks. Saya juga menggunakan strip_tags pada
EducationForm untuk membersihkan tag HTML dari nama institusi
dan program studi, serta menolak hasil yang kosong.

strip_tags bukan jaminan keamanan untuk semua konteks. Penggunaan
textContent tetap diperlukan agar data ditampilkan dengan aman.

#### Implementasi

Saya menerapkan AJAX pada bagian Education dengan:
- Endpoint JSON berisi data pendidikan, jumlah star, dan status
  star pengguna yang sedang login.
- Pencarian institusi dengan debouncing 300 milidetik.
- Tampilan loading, hasil kosong, dan pesan gagal memuat data.
- Modal tambah pendidikan yang mengirim FormData melalui fetch.
- CSRF token yang ikut dikirim bersama data form.
- Pembaruan daftar tanpa reload setelah penambahan berhasil.
- Toast berhasil atau gagal dan pesan validasi pada modal.
- Validasi EducationForm dan rendering menggunakan textContent.
- Pembatasan akses: superuser dapat menambah, mengedit, dan
  menghapus; Editor dapat mengedit; pengguna biasa dapat
  memberikan star; pengunjung dapat melihat dan mencari data.

#### Pengujian manual

Pengujian yang telah saya lakukan:
- Menambahkan pendidikan melalui modal dan melihat kartu baru
  muncul tanpa reload.
- Memasukkan <b></b> sebagai nama institusi dan memastikan
  validasi menolak hasil yang kosong setelah tag dibersihkan.
- Memasukkan tag gambar dengan atribut onerror dan memastikan
  input ditolak tanpa menjalankan popup JavaScript.
- Memastikan pengunjung dapat melihat serta mencari pendidikan,
  tetapi tidak melihat tombol pengelolaan data.
- Menguji akses pengguna biasa dan akun Editor.
- Menyimpan pendidikan melalui akun Editor.
- Membuka URL edit dengan akun biasa dan menerima 403 Forbidden.
- Mencari institusi yang tidak ada, lalu mengosongkan pencarian
  untuk menampilkan kembali daftar.
- Pengujian kondisi koneksi offline.

#### Penggunaan AI

Saya menggunakan ChatGPT untuk membantu memahami dan mengerjakan AJAX secara bertahap. AI membantu memberikan contoh endpoint JSON, validasi form, modal, pencarian dengan debouncing, dan pengiriman form melalui fetch. Saya menjalankan pengujian manual di browser serta pmeriksaan Django dan sintaks JavaScript.

### Tutorial 7 — Django REST Framework

Projects sekarang menggunakan Django REST Framework 3.18.3 dengan database dan
model yang sudah ada. Penyesuaian terhadap contoh tutorial: ID Project berupa
integer, dan field portofolio musik adalah `title`, `role`, `year`, `description`,
serta `spotify_url`. Tidak ada migrasi model atau penggantian data.

#### Kontrak API

| Method | URL | Akses |
| --- | --- | --- |
| GET | `/api/v1/projects/?title=...` | Semua pengunjung |
| POST | `/api/v1/projects/` | Superuser |
| GET | `/api/v1/projects/<id>/` | Semua pengunjung |
| PUT / PATCH | `/api/v1/projects/<id>/` | Superuser |
| DELETE | `/api/v1/projects/<id>/` | Superuser |
| POST | `/api/v1/projects/<id>/star/` | Pengguna login |

`ProjectSerializer` menghasilkan objek JSON datar dengan `id`, bukan `pk` atau
`fields`. `star_count`, `is_starred`, dan `starred_by_names` bersifat read-only.
Validasi teks dijalankan kembali pada serializer karena API tidak menjalankan
validasi `ProjectForm`. Link Spotify tetap divalidasi sebagai URL.

API menggunakan `SessionAuthentication`. Operasi tulis mengirim `X-CSRFToken`.
Permission server membatasi pengelolaan Projects kepada superuser; menjadi staff
atau anggota Editor tidak memberi izin mengubah Projects. Hak Editor pada
Education yang sudah ada tetap dipertahankan. Kelas
`IsPortfolioOwnerOrEditorOrReadOnly` disiapkan untuk penerapan DRF pada bagian
pilihan di Tugas 6; Education saat ini masih memakai endpoint sebelumnya.

Frontend Projects memakai fetch untuk daftar, tambah, hapus, dan toggle star.
Pencarian menggunakan debounce 300 ms dan AbortController, sedangkan teks
menggunakan textContent. Modal dan toast tetap dipakai. Respons DELETE 204 tidak
diparsing sebagai JSON. PUT/PATCH tersedia di API/Browsable API; tutorial ini
tidak menambahkan modal edit Projects baru. Endpoint lama tetap tersedia agar
halaman dan pekerjaan sebelumnya tidak dihapus.

#### Menjalankan dan memeriksa

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py test main.tests_api --verbosity 2
python manage.py test main
python manage.py runserver
```

Hasil pemeriksaan lokal: 13 tes API dan seluruh 36 tes app `main` lulus.
Cakupannya meliputi GET publik, pencarian, 404, create, PUT/PATCH/DELETE, validasi,
star, field read-only, penolakan akses, method yang salah, dan session dengan/tanpa
CSRF. Tes lama diperbarui agar memeriksa JSON untuk daftar yang kini dirender AJAX,
profil dengan galeri, serta redirect registrasi ke login.

Pemeriksaan browser dilakukan untuk pemuatan Projects sebagai pengunjung dan
pencarian tanpa hasil. Operasi tulis diverifikasi melalui tes API; pemeriksaan
manual seluruh alur login/modal/star/delete di browser dan deployment PWS masih
perlu dilakukan sebelum pengumpulan. Belum dilakukan push atau deployment dalam
pengerjaan ini.

#### Bantuan AI

ChatGPT membantu menyesuaikan contoh Tutorial 7 dengan model portofolio musik. Dokumentasi ini membedakan tes otomatis yang dijalankan dari pemeriksaan manual yang belum dilakukan.

### Tugas 6

Pada tugas ini, bagian **Education** dari Tugas 3–5 menggunakan Django REST
Framework. Model dan data pendidikan yang sudah ada tetap digunakan. Halaman
Projects dari Tutorial 7 serta bagian portofolio lainnya tetap tersedia.

#### 1. REST serta perbedaan PUT dan PATCH

REST (Representational State Transfer) adalah gaya arsitektur untuk merancang
komunikasi antara klien dan server. Data dipandang sebagai resource yang memiliki
alamat, misalnya `/api/v1/education/`. Tindakan terhadap resource dinyatakan
melalui method HTTP, seperti GET untuk membaca dan DELETE untuk menghapus.

Mengembalikan JSON saja belum membuat API menjadi RESTful karena JSON hanya
format representasi data. Desain resource, penggunaan method, status HTTP, dan
prinsip seperti stateless juga perlu diperhatikan. Implementasi ini menggunakan
session Django, sehingga belum sepenuhnya stateless karena informasi session
masih disimpan di server.

PUT digunakan untuk mengirim representasi lengkap data yang akan diperbarui.
Contohnya, mengganti institusi, program, tahun masuk, dan tahun selesai sekaligus.
Pada serializer ini, PUT harus menyertakan seluruh field wajib. Field opsional
tetap mengikuti aturan serializer, sehingga PUT tidak otomatis mengosongkan
semua field opsional yang tidak dikirim.

PATCH digunakan untuk pembaruan sebagian, misalnya hanya mengganti `program`
menjadi `Sistem Informasi`. Field yang tidak dikirim tetap menggunakan nilai
sebelumnya. Modal edit Education menggunakan PATCH.

#### 2. Peran serializer dan keuntungannya

Serializer mengubah objek model menjadi data Python yang dapat dirender DRF
sebagai JSON. Pada arah sebaliknya, serializer memvalidasi input sebelum membuat
atau memperbarui objek model. `EducationSerializer` menggunakan ModelSerializer
agar definisi field dan operasi penyimpanan dasar dapat mengikuti model Education.

Dibandingkan merakit dictionary dengan JsonResponse, serializer membantu menjaga
struktur respons tetap konsisten dan menyatukan aturan validasi input. Daftar
field ditulis eksplisit agar hanya data yang diperlukan yang ditampilkan.
`star_count` dan `is_starred` dihitung melalui SerializerMethodField dan tidak
bisa diubah melalui payload klien.

Validasi `validate_institution` dan `validate_program` membersihkan tag HTML dengan
strip_tags, lalu menolak hasil yang kosong. Validasi serializer perlu ditulis
tersendiri karena API tidak menjalankan metode `clean_<field>` milik ModelForm.
Teks pada halaman ditampilkan menggunakan textContent; strip_tags sendiri bukan
jaminan keamanan untuk semua konteks HTML.

#### 3. Autentikasi dan otorisasi

Autentikasi menentukan siapa pengguna yang mengirim permintaan. Pada API ini,
SessionAuthentication menggunakan session login Django untuk mengenali pengguna.
Otorisasi menentukan tindakan yang boleh dilakukan pengguna tersebut.

Endpoint daftar dan detail menggunakan IsPortfolioOwnerOrEditorOrReadOnly:
- Pengunjung dapat membaca daftar dan detail.
- Pengguna biasa juga dapat memberikan atau membatalkan star.
- Editor dapat mengubah data dengan PUT/PATCH, tetapi tidak boleh membuat atau
  menghapus pendidikan.
- Superuser dapat membuat, mengubah, dan menghapus pendidikan.

Endpoint star menggunakan IsAuthenticated dan mengambil akun dari request.user,
bukan dari ID pengguna yang dikirim klien. Menyembunyikan tombol hanya membantu
tampilan. Pengguna masih bisa mengirim request langsung ke URL API, sehingga
permission di server tetap harus memeriksa setiap tindakan.

#### 4. SessionAuthentication, CSRF, dan pengujiannya

Browser dapat mengirim cookie session secara otomatis. Karena itu, penyerang
berpotensi membuat browser pengguna yang sedang login mengirim permintaan yang
tidak diinginkan. Token CSRF membantu server memeriksa permintaan tersebut.
Penggunaan JSON atau AJAX tidak menghilangkan kebutuhan perlindungan CSRF.

Setiap operasi tulis dari halaman Education mengirim header X-CSRFToken.
Token diperoleh dari input tersembunyi yang dihasilkan oleh tag csrf_token,
termasuk pada halaman pengguna biasa yang hanya bisa memberikan star.

force_authenticate membantu menguji hak akses dengan menetapkan pengguna secara
langsung, tetapi melewati proses autentikasi session yang sesungguhnya. Karena
itu, tes tersebut belum membuktikan perlindungan CSRF. Tes tambahan menggunakan
APIClient(enforce_csrf_checks=True) dan login() untuk memastikan POST tanpa token
ditolak dengan 403 dan database tidak berubah. Tes juga memastikan POST dengan
token yang valid berhasil.

#### Implementasi dan endpoint

| Method | Endpoint | Fungsi | Akses |
| --- | --- | --- | --- |
| GET | `/api/v1/education/?institution=...` | Daftar dan pencarian | Semua pengunjung |
| POST | `/api/v1/education/` | Tambah pendidikan | Superuser |
| GET | `/api/v1/education/<id>/` | Detail pendidikan | Semua pengunjung |
| PUT / PATCH | `/api/v1/education/<id>/` | Ubah pendidikan | Editor dan superuser |
| DELETE | `/api/v1/education/<id>/` | Hapus pendidikan | Superuser |
| POST | `/api/v1/education/<id>/star/` | Toggle star | Pengguna login |

ID Education berupa integer. Respons menggunakan status 201 untuk penambahan,
400 untuk input tidak valid, 403 untuk akses yang ditolak, 404 untuk objek yang
tidak ditemukan, dan 204 tanpa body setelah penghapusan berhasil.

Halaman Education menggunakan fetch untuk daftar, pencarian, tambah, edit, star,
dan hapus. Pencarian tetap memakai debounce 300 ms dan AbortController. Modal
edit mengambil detail terbaru sebelum menampilkan isian. Tahun selesai yang
kosong dikirim sebagai null, dan tahun selesai tidak boleh mendahului tahun masuk.
Toast menampilkan keberhasilan maupun kesalahan API. Respons 204 tidak diparsing
sebagai JSON. Nama institusi dan program ditampilkan sebagai teks menggunakan
textContent.

#### Menjalankan dan menguji

Jalankan dari folder yang berisi manage.py:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py check
python manage.py collectstatic --noinput
python manage.py test main.tests_education_api --verbosity 2
python manage.py test main
python manage.py runserver
```

Buka `/education/` untuk halaman Education atau `/api/v1/education/` untuk
Browsable API. Gunakan akun dengan peran yang sesuai untuk mencoba operasi tulis.

Hasil pengujian otomatis lokal: **47 tes lulus**, termasuk **11 tes Education**
dan tes Projects dari Tutorial 7. Pengujian Education mencakup empat peran,
isi database setelah akses ditolak, validasi teks dan tahun, PUT/PATCH, star,
field read-only, CSRF, serta ketersediaan tombol dan modal sesuai peran.
Sintaks JavaScript juga telah diperiksa. Hasil ini tidak menggantikan pengujian
manual seluruh alur browser maupun pengecekan deployment PWS.

#### Bantuan AI

Saya menggunakan ChatGPT untuk memahami konsep DRF, mendiskusikan langkah
pengerjaan, serta membantu implementasi dan pengujian API Education.

Strategi prompting yang digunakan adalah memberikan tautan instruksi Tugas 6,
meminta pengerjaan bertahap, dan meminta kesempatan untuk memeriksa perubahan
sebelum setiap commit. Bantuan meliputi serializer, permission, endpoint API,
integrasi AJAX dan modal edit, pengujian, serta penyusunan draf dokumentasi.

Contoh permintaan dalam percakapan:
- “tolong ini dan commit berkala tp aku mau cek dl sblm commit, yaa”
- “ok commit dl pk tugas 6: add ...”
- “tambah aja tugas 6 jgn dr awal d gnti smw”

Kode dan penjelasan dari AI tetap perlu diperiksa terhadap instruksi tugas dan
struktur proyek. Tes otomatis membantu memeriksa perilaku API, tetapi tidak
menjamin seluruh interaksi browser dan kondisi deployment sudah teruji.
