# FINAL PROJECT REPORT: SIMPLE LMS

## 1. Identitas
- **Nama:** Puriarto Bagas Widiantoro
- **NIM:** A11.2023.14962
- **Mata Kuliah:** Pemrograman Sisi Server 
- **URL Repository:** https://github.com/widipuriarto/simple-lms](https://github.com/widipuriarto/simple-lms)

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

*Seluruh dokumentasi gambar (*assets*) diambil secara langsung dari hasil pengujian *live* sistem dan antarmuka Swagger API.*

### A. Komponen Wajib (Fondasi Project)

#### 1. Project dapat dijalankan dengan Docker Compose
**Deskripsi Implementasi:**
Keseluruhan sistem *Simple LMS* ini dibungkus (*containerized*) menggunakan Docker. Komponen-komponen seperti *web server* (Django), *database* (PostgreSQL & MongoDB), *message broker* (RabbitMQ), dan *cache* (Redis) diorkestrasi secara terpusat melalui konfigurasi file `docker-compose.yml`.

**Bukti Pengujian:**
- ![Docker ps](assets/docker_ps.png)
*Gambar di atas adalah output dari perintah `docker-compose ps` yang menunjukkan seluruh container beroperasi mulus (berada pada state Up).*

#### 2. Database PostgreSQL berjalan dan migration berhasil
**Deskripsi Implementasi:**
Sebagai media penyimpanan relasional utama, aplikasi ini dihubungkan secara eksklusif ke instance PostgreSQL. Skema tabel dikonstruksi secara otomatis melalui sistem *Migration* bawaan Django yang dioperasikan sesaat setelah kontainer database siap.

**Bukti Pengujian:**
- ![ShowMigrations](assets/show-migrations.png)
*Tangkapan layar di atas memperlihatkan deretan checklist `[X]` pada aplikasi `courses` dan aplikasi inti lainnya, membuktikan bahwa skema database berhasil diterapkan sepenuhnya ke dalam PostgreSQL.*

#### 3. Model Utama LMS (User, Category, Course, Lesson, Enrollment, Progress)
**Deskripsi Implementasi:**
Sebagai fondasi dari sistem *Learning Management System*, kami telah mendefinisikan seluruh model data esensial yang saling berelasi. Model-model tersebut mencakup: entitas `User` (dikembangkan dengan profil Role), `Category` (kategori kursus), `Course` (entitas kursus inti), `Lesson` (sub-materi kursus), `Enrollment` (pendaftaran siswa), dan `Progress` (jejak penyelesaian materi).

**Bukti Pengujian:**
- ![Django Admin](assets/django-admin.png)
*Halaman beranda Django Admin yang menampilkan daftar seluruh tabel model LMS yang telah diregistrasikan dan siap dikelola (CRUD).*

#### 4. Authentication JWT Berjalan & Role admin, instructor, student diterapkan
**Deskripsi Implementasi:**
Aplikasi mengamankan *endpoints* dengan menggunakan *JSON Web Token* (JWT) via pustaka `ninja_simple_jwt`. Untuk manajemen hak akses atau *Role-Based Access Control* (RBAC), pengguna dibagi menjadi tiga tingkatan *role*:
- **Admin**: Wewenang absolut (termasuk penghapusan *Course*).
- **Instructor**: Diizinkan untuk merancang dan mempublikasikan *Course* beserta *Lesson*.
- **Student**: Terbatas hanya pada akses konsumsi (*enroll* dan *view* materi).

**Bukti Pengujian:**
- ![JWT Token](assets/jwt-token.png)
*Hasil login akun tipe student yang memunculkan token Bearer (Access & Refresh token).*
- ![Role Forbidden](assets/role-forbidden.png)
*Hasil penolakan hak akses (Role Forbidden / HTTP 403) ketika akun tipe student mencoba memaksa membuat sebuah course.*
- ![Role Success](assets/role-success.png)
*Hasil kesuksesan otorisasi (Role Success) ketika akun tipe instructor sukses membuat sebuah course.*
- ![Role Admin](assets/admin-success.png)
*Hasil pengujian wewenang admin yang sukses menghapus course secara mutlak.*

#### 5. Endpoint course, lesson, enrollment, progress berjalan
**Deskripsi Implementasi:**
Sistem menyediakan antarmuka REST API komprehensif. *Course API* melayani pencarian dan CRUD. *Enrollment API* mencatat pendaftaran siswa agar mereka berhak mengakses materi. Sementara *Progress API* mencatat jejak penyelesaian tiap materi (*lesson*).

**Bukti Pengujian:**
- ![course-list](assets/course-list.png)
*Hasil eksekusi `GET /api/v1/protected/courses` yang menampilkan keseluruhan daftar kursus secara publik.*
- ![enrollment-success](assets/enrollment-success.png)
*Hasil eksekusi `POST /api/v1/protected/enrollments` saat Student berhasil mendaftarkan diri pada sebuah kursus.*

#### 6. Swagger/OpenAPI dapat diakses
**Deskripsi Implementasi:**
Dokumentasi API interaktif dirender otomatis melalui fitur *OpenAPI Schema* bawaan `django-ninja`. Kehadiran Swagger UI menjadi sarana vital untuk mempermudah eksplorasi *endpoints*, struktur JSON, dan melakukan pengujian *real-time*.

**Bukti Pengujian:**
- ![Swagger UI](assets/swagger-ui.png)
*Halaman utama Swagger UI yang memuat daftar lengkap berbagai endpoint API yang terekspos dari backend LMS.*

---

### B. Fitur Tambahan: Paket 1 – LMS Experience

#### 1. Database & Model Enhancement (Prasyarat)
**Deskripsi Implementasi:**
Sebagai fondasi paket ekstensi, skema `Course` ditambahkan variabel enumerasi `level` dan `status`. Tiga buah entitas pendukung yang benar-benar baru (`Section`, `Review`, dan `Wishlist`) divalidasi dan dilempar (*migrate*) ke database.

**Bukti Pengujian:**
- ![Django Admin Paket 1](assets/django-admin-models.png)
*Penampakan mutakhir portal admin yang telah merangkum model tabel-tabel ekstensi baru (Reviews, Sections, Wishlists).*

#### 2. Search, filter, dan sorting course lanjutan
**Deskripsi Implementasi:**
*Course mudah ditemukan berdasarkan keyword, category, instructor, level, status, dan sorting.* Kami mengimplementasikan logika penyaringan menggunakan antarmuka `django-ninja` (Schema Filter) dikombinasikan dengan pencarian teks penuh (mencari ke dalam judul dan deskripsi) via objek klausa `Q` pada ORM Django di rute `GET /courses`.

**Bukti Pengujian:**
- ![Search Field Filter Swagger](assets/swagger-filter-search.png)
*Tampilan form filter pada antarmuka interaktif Swagger.*
- ![Filter Swagger](assets/swagger-filter.png)
*Hasil pengujian eksekusi endpoint `GET /courses` dengan memberikan kombinasi nilai input spesifik di parameter `level`, `status`, dan `search`.*

#### 3. Rating, review, dan wishlist course
**Deskripsi Implementasi:**
*Student dapat memberi review dan menyimpan course favorit.* Fitur ini direalisasikan melalui penciptaan entitas `Review` (mencatat bintang/komentar) dan `Wishlist` (daftar keinginan). Kami menggunakan proteksi validasi pendaftaran (*enrollment validation*) agar hanya siswa yang terdaftar yang boleh memberikan *Review*.

**Bukti Pengujian:**
- ![Review Course Swagger](assets/swagger-review.png)
*Hasil eksekusi endpoint pengiriman atau pembacaan ulasan (Review) pada sebuah kursus tertentu.*
- ![Wishlist Course Swagger](assets/swagger-wishlist.png)
*Hasil eksekusi endpoint `GET /wishlist` yang memunculkan daftar kursus favorit milik seorang siswa.*

#### 4. Curriculum dan progress belajar detail
**Deskripsi Implementasi:**
*Course punya section/module dan progress dihitung lebih akurat.* Struktur hierarki kursus yang tadinya berderet lurus, kini dipecah bertingkat menjadi `Course -> Section -> Lesson`. Untuk penghitungan persentase ketuntasan (0.0% hingga 100.0%), kami tidak menggunakan kalkulasi kasual, melainkan algoritma matematis komputasi murni dari titik pusat *backend*.

**Bukti Pengujian:**
- ![Nested Curriculum Swagger](assets/swagger-curriculum.png)
*Bukti respon berjenjang JSON (Nested Schema) pada saat pemanggilan Detail Course, yang memperlihatkan susunan Section dan Lesson anak-anaknya secara elegan.*

#### 5. Student dashboard
**Deskripsi Implementasi:**
*Ringkasan course aktif, progress, dan rekomendasi.* Endpoint `/dashboard/student` diciptakan secara eksklusif untuk merekapitulasi seluruh perjalanan belajar siswa secara *real-time*. Logika *backend* melakukan sapuan kueri untuk mengelompokkan kursus menjadi: *Active* (Sedang dipelajari), *Completed* (Tamat 100%), dan merekomendasikan kursus-kursus (*Recommended*) berdasar kategori yang sedang ia tekuni.

**Bukti Pengujian:**
- ![Student Dashboard Swagger](assets/swagger-dashboard.png)
*Data JSON hasil `GET /dashboard/student` yang merangkum keseluruhan informasi holistik milik seorang siswa di satu layar.*

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
