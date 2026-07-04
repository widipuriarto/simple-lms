# FINAL PROJECT REPORT: SIMPLE LMS

## 1. Identitas
- **Nama:** Puriarto Bagas Widiantoro
- **NIM:** A11.2023.14962
- **Kelas:** 
- **URL Repository:** [Link Repository GitHub]

## 2. Deskripsi Project
Simple LMS adalah sebuah sistem manajemen pembelajaran berbasis *backend* yang mengusung arsitektur *microservices-ready*. Dibangun dengan kerangka kerja Django Ninja modern, proyek ini menyediakan fungsionalitas mumpuni; mulai dari hierarki materi (*Section & Lesson*) yang terstruktur, perekaman jejak progres (*Progress*) siswa yang akurat secara matematis, hingga fitur komunitas seperti sistem Ulasan (*Review*) dan Daftar Keinginan (*Wishlist*).

Keseluruhan proyek telah dikontainerisasi secara penuh menggunakan ekosistem Docker yang menghubungkan *web server* Django dengan relasi database PostgreSQL, basis data NoSQL MongoDB untuk *log* aktivitas, mesin antrean tugas RabbitMQ, dan lapisan *caching* kueri Redis.

## 3. Fitur Dasar yang Sudah Berjalan
Berikut adalah fondasi fitur dasar penyokong sistem yang sukses beroperasi:
1. **Dockerized Environment:** Sistem berjalan sempurna dan terorkestrasi di atas Docker Compose.
2. **PostgreSQL Database:** Sistem penyimpanan relasional yang sukses ter-migrasi.
3. **Authentication JWT:** Mengamankan akses *endpoint* via token *Bearer*.
4. **Role-Based Access Control (RBAC):** Proteksi wewenang Admin, Instructor, dan Student terintegrasi dengan kokoh.
5. **Course API:** Menyediakan opsi pencarian hingga pengelolaan konten materi (CRUD).
6. **Enrollment & Progress:** Siswa diwajibkan mendaftar sebelum membaca kursus, dan penyelesaian materinya terekam.
7. **Swagger/OpenAPI:** Seluruh interaksi *endpoint* terdokumentasi otomatis.

## 4. Fitur Tambahan yang Dipilih (Paket 1 - LMS Experience)
| No | Fitur Tambahan | Kategori | Poin | Status |
| :-: | :--- | :--- | :-: | :--- |
| 1 | Search, filter, dan sorting course lanjutan | Paket 1 | 12 | Selesai |
| 2 | Rating, review, dan wishlist course | Paket 1 | 12 | Selesai |
| 3 | Curriculum dan progress belajar detail | Paket 1 | 15 | Selesai |
| 4 | Student dashboard | Paket 1 | 12 | Selesai |
| **Total**| | | **51** | **100% Selesai** |

## 5. Penjelasan Implementasi & Bukti Pengujian (Screenshots)

*Semua dokumentasi visual (assets) diambil dari hasil pengujian murni melalui sistem dan antarmuka Swagger.*

### A. Komponen Wajib (Fondasi)
**1. Docker Compose dan Database PostgreSQL**
Sistem berjalan stabil secara orkestrasi via `docker-compose ps`. Migrasi tabel inti (`courses`, `auth`, dll) sukses ter- *mapping* di basis data PostgreSQL.
- ![Docker ps](assets/docker_ps.png) *(Status semua container UP)*
- ![ShowMigrations](assets/show-migrations.png) *(Tabel sukses tercipta di DB)*

**2. Model Utama LMS (Django Admin)**
Objek utama `User`, `Category`, `Course`, `Lesson`, `Enrollment`, `Progress` dapat dioperasikan penuh di portal Django Admin.
- ![Django Admin](assets/django-admin.png) *(Halaman Administrator LMS Utama)*

**3. Autentikasi JWT & Role (RBAC)**
Kami memvalidasi tiga peran (Admin, Instructor, Student) dengan skenario penolakan hak akses (*Student* tidak diizinkan menciptakan/menghapus kursus).
- ![JWT Token](assets/jwt-token.png) *(Token Berhasil Digenerate)*
- ![Role Forbidden](assets/role-forbidden.png) *(Akses Ilegal Ditolak 403)*
- ![Role Success](assets/role-success.png) *(Akses Legal Instructor 201)*
- ![Role Admin](assets/admin-success.png) *(Akses Legal Admin Hapus Course)*

**4. Endpoint Core (Course & Enrollment)**
API inti merespons daftar kursus dan perintah pendaftaran (*enrollment*) dengan baik.
- ![Course List](assets/course-list.png) *(Daftar Kursus Inti)*
- ![Enrollment Success](assets/enrollment-success.png) *(Pendaftaran Berhasil)*
- ![Swagger UI](assets/swagger-ui.png) *(Keseluruhan Antarmuka API Docs)*

### B. Fitur Tambahan Paket 1 (LMS Experience)
**1. Database Enhancement & Relasi Baru**
Skema `Course` ditambahkan atribut `level` & `status`. Tiga buah entitas baru (`Section`, `Review`, dan `Wishlist`) sukses bermigrasi.
- ![Django Admin Paket 1](assets/django-admin-models.png) *(Tabel Tambahan Muncul di Portal Admin)*

**2. Search, Filter, dan Sorting (12 Poin)**
Penyaringan diimplementasikan pada *schema* `django-ninja` dan dukungan pencarian teks penuh (di Judul & Deskripsi) mengandalkan klausa OR via objek `Q` dari Django ORM.
- ![Search Field Filter](assets/swagger-filter-search.png)
- ![Filter Swagger](assets/swagger-filter.png)

**3. Rating, Review, dan Wishlist (12 Poin)**
Siswa yang sukses mendaftar bisa membintangi kursus (*Review*), atau memasukkan kursus publik ke dalam penyimpanan (*Wishlist*).
- ![Review Course](assets/swagger-review.png)
- ![Wishlist Course](assets/swagger-wishlist.png)

**4. Curriculum (Nested) dan Progress (15 Poin)**
Materi pelajaran beralih format menjadi berjenjang/bersarang (`Course -> Section -> Lesson`). Selain itu, kalkulasi kelulusan diukur mutlak di *backend* (jumlah *Lesson* yang tamat dibagi total *Lesson*).
- ![Nested Curriculum](assets/swagger-curriculum.png)

**5. Student Dashboard (12 Poin)**
Sebuah *endpoint* raksasa tunggal di rute `/dashboard/student` diciptakan untuk meringkas 3 kondisi: Kursus aktif, Kursus yang sudah selesai (Tamat 100%), dan Daftar rekomendasi kursus di kategori serupa.
- ![Student Dashboard](assets/swagger-dashboard.png)

## 6. Cara Menjalankan Project (Docker)
Langkah-langkah mereplikasi ekosistem proyek ini:
1. Bentuk file rahasia dari cetakannya: `cp .env.example .env`
2. Bangun dan luncurkan susunan kontainer: `docker-compose up -d --build`
3. Kirimkan skema tabel terbaru: `docker-compose exec web python manage.py migrate`
4. Tabur bibit data percontohan (*seeding*): `docker-compose exec web python manage.py seed`

## 7. Akun Demo Pengujian
Skrip *seeding* menyediakan konfigurasi identitas praktis:
| Peran | Username | Password |
| :--- | :--- | :--- |
| **Administrator** | `admin` | `password123` |
| **Instructor** | `instructor` | `123` |
| **Student** | `student` | `123` |

## 8. Endpoint Penting
Seluruh antarmuka ini wajib disematkan *Bearer Token* di bagian Auth.
- `POST /api/v1/auth/token` : Login otentikasi.
- `GET /api/v1/protected/courses` : Mengambil katalog kursus.
- `GET /api/v1/protected/courses/{id}` : Mengupas hierarki modul sebuah kursus secara mendalam.
- `GET /api/v1/protected/dashboard/student` : Merekap rute perjalanan (Dashboard) khusus untuk siswa.
- `GET /api/v1/protected/courses/{id}/progress` : Melihat persentase ketuntasan materi.

## 9. Kendala dan Solusi
Beberapa rintangan teknis yang berhasil diatasi sepanjang masa pengerjaan:
1. **Transmisi Sinyal Inotify Docker Windows Terputus:** 
   Perubahan baris kode di `api.py` dan `schemas.py` acap kali tak terekam oleh *StatReloader* karena hilangnya deteksi sinyal simpan-file (*inotify*) antara Windows dan kontainer Linux. **Solusi:** Memaksa siklus penyegaran *web container* secara manual (`docker-compose restart web`) pasca suntingan krusial.
2. **Pydantic Validation Error (Type-Safety) pada Schema:**
   Sistem melempar Error 500 karena objek PostgreSQL bertipe *datetime* dipaksa masuk ke dalam *schema* bertipe `str` murni, dan `CourseOut` tidak mengenali objek `User`/`Category`. **Solusi:** Menukar tipe pada *schema* menjadi `datetime` dari *library* bawaan, dan menginjeksi metode pelacak khusus (`resolve_instructor` / `resolve_category`).
3. **Konflik Array di Role-Based Access Control:**
   *Endpoint* menolak token *legal* (403 Forbidden) akibat metode *decorator* pelindung mencoba membandingkan string secara mentah dengan sebuah *list* (`"student" == ["student"]`). **Solusi:** Melakukan re-faktor total terhadap algoritma `role_required` agar merujuk pada logika `in list` (himpunan keanggotaan).

## 10. Kesimpulan
Menggelar konstruksi *Simple LMS Backend* merupakan pembelajaran luar biasa ihwal arsitektur *microservices*, perakitan kontainer, pengetatan gerbang keamanan (*JWT & RBAC*), serta kemewahan kecepatan *API Design* abad ke-21 menggunakan `django-ninja` disokong ketangguhan validasi *Pydantic*. Proyek ini menjelma tak hanya sekadar tugas belaka, melainkan miniatur mahakarya kesiapan industri.
