# Draft Dokumentasi Final Project: Simple LMS

Dokumen ini adalah coretan kerja (draft) yang akan berisi seluruh penjelasan, pengujian, dan screenshot untuk setiap fitur yang telah diimplementasikan. Pada tahap akhir, isi dokumen ini akan dirangkum untuk menyusun `README.md` dan `FINAL_PROJECT_REPORT.md`.

## 1. Komponen Wajib (Fondasi Project) - 30 Poin

| Status | Item Wajib | Poin | Catatan / Link Dokumentasi |
| :---: | :--- | :---: | :--- |
| [x] | Project dapat dijalankan dengan Docker Compose | 5 | - |
| [x] | Database PostgreSQL berjalan dan migration berhasil | 4 | - |
| [x] | Model utama: User, Category, Course, Lesson, Enrollment, Progress | Basis | - |
| [x] | Authentication JWT berjalan | 4 | - |
| [x] | Role admin, instructor, student diterapkan dengan benar | 4 | - |
| [x] | Endpoint course, lesson, enrollment, progress berjalan | 5 | - |
| [ ] | README berisi cara menjalankan, akun demo, dan endpoint utama | 4 | - |
| [x] | Swagger/OpenAPI dapat diakses | 2 | - |
| [x] | Struktur project rapi, tidak hardcode konfigurasi sensitif | 2 | - |

---

### Penjelasan Komponen Wajib

#### 1. Project dapat dijalankan dengan Docker Compose (5 Poin)
**Deskripsi Implementasi:**
Keseluruhan sistem *Simple LMS* ini dibungkus (*containerized*) menggunakan Docker. Komponen-komponen seperti *web server* (Django), *database* (PostgreSQL & MongoDB), *message broker* (RabbitMQ), dan *cache* (Redis) diorkestrasi secara terpusat melalui file `docker-compose.yml`.

**Langkah Menjalankan Project:**
Proyek dijalankan dengan perintah berikut di terminal root:
```bash
docker-compose up -d --build
```
Untuk memverifikasi bahwa semua *container* berjalan normal tanpa ada yang berhenti (*exited*), kami menggunakan perintah `docker-compose ps`.

**Bukti Pengujian:**
- ![Docker ps](assets/docker-ps.png) 
Gambar di atas adalah *output* dari perintah `docker-compose ps` yang menunjukkan seluruh *container* berada pada *state* `Up`.

#### 2. Database PostgreSQL berjalan dan migration berhasil (4 Poin)
**Deskripsi Implementasi:**
Sebagai media penyimpanan relasional utama, aplikasi ini terhubung ke instance PostgreSQL. Skema tabel dikonstruksi secara otomatis melalui sistem *Migration* bawaan Django yang dioperasikan sesaat setelah kontainer database siap.

**Pembuktian Migrasi:**
Pengecekan riwayat migrasi dilakukan melalui *web container* dengan perintah:
```bash
docker-compose exec web python manage.py showmigrations
```

**Bukti Pengujian:**
- ![ShowMigrations](assets/show-migrations.png)
Tangkapan layar di atas memperlihatkan deretan *checklist* `[X]` pada aplikasi `courses` dan aplikasi inti lainnya, membuktikan bahwa skema database berhasil diterapkan sepenuhnya ke dalam PostgreSQL.

#### 3. Model Utama LMS (User, Category, Course, Lesson, Enrollment, Progress)
**Deskripsi Implementasi:**
Sebagai fondasi dari sistem *Learning Management System*, kami telah mendefinisikan seluruh model data esensial yang saling berelasi. Model-model tersebut mencakup: entitas `User` (dikembangkan lebih lanjut dengan profil Role), `Category` (kategori kursus), `Course` (entitas kursus), `Lesson` (sub-materi kursus), `Enrollment` (pendaftaran siswa), dan `Progress` (jejak penyelesaian materi).

**Pembuktian Model:**
Keseluruhan model ini telah diregistrasikan ke dalam panel Django Admin sehingga dapat dipantau dan dikelola (CRUD) secara langsung melalui antarmuka grafis administrator.

**Bukti Pengujian:**
- [Django Admin](assets/django-admin.png)
halaman beranda Django Admin yang menampilkan daftar model LMS.

#### 4. Authentication JWT Berjalan (4 Poin) & 5. Role admin, instructor, student diterapkan (4 Poin)
**Deskripsi Implementasi:**
Aplikasi mengamankan *endpoints* dengan menggunakan *JSON Web Token* (JWT) via `ninja_simple_jwt`. Untuk manajemen hak akses (RBAC), pengguna dibagi menjadi tiga tingkatan *role* yang disematkan di dalam entitas `UserProfile`:
- **Admin**: Memiliki wewenang absolut termasuk penghapusan kursus.
- **Instructor**: Diberikan hak untuk merancang dan mendistribusikan *Course* beserta *Lesson*.
- **Student**: Terbatas pada akses konsumsi (*enroll* dan *view* materi).

**Langkah Pengujian Auth dan Role:**
Pengujian dilakukan menggunakan Swagger UI (`/api/v1/docs`) atau Postman dengan alur berikut:
1. Memanggil *endpoint* `POST /api/v1/auth/sign-in` menggunakan akun *Student*, *Instructor*, dan *Admin*.
2. Mendapatkan token `access` dari respons JWT.
3. Mencoba membuat `Course` (membutuhkan otorisasi *Instructor*). Jika yang mengakses adalah *Student*, maka akan ditolak.
4. Mencoba menghapus `Course` (membutuhkan otorisasi *Admin*). Jika yang mengakses adalah *Student* atau *Instructor*, maka akan ditolak.

**Bukti Pengujian yang Dibutuhkan (Screenshots):**

- ![JWT Token](assets/jwt-token.png)
hasil login student yang memunculkan token Bearer.
- ![Role Forbidden](assets/role-forbidden.png)
hasil role forbidden ketika student mencoba membuat course.
- ![Role Success](assets/role-success.png)
hasil role success ketika instructor sukses membuat course.
- ![Role Admin](assets/admin-success.png)
hasil role admin ketika sukses menghapus course.

#### 6. Endpoint course, lesson, enrollment, progress berjalan (5 Poin)
**Deskripsi Implementasi:**
Sistem menyediakan antarmuka REST API yang komprehensif untuk mengelola inti dari ekosistem pembelajaran (*Learning Management System*):
- **Course API**: Mengelola entitas kursus, mencakup fungsi pencarian, *filtering*, dan operasi CRUD (Create, Read, Update, Delete) sesuai wewenang.
- **Lesson API**: Menangani penambahan dan pengambilan sub-materi pelajaran dalam sebuah kursus.
- **Enrollment API**: Mencatat pendaftaran *Student* pada kursus tertentu. Sistem akan menolak akses materi jika *Student* belum melakukan *enrollment*.
- **Progress API**: Mencatat jejak pembelajaran *Student*, menandai status penyelesaian (*completion*) dari setiap *Lesson* yang telah dipelajari.

**Pembuktian Endpoint Utama:**
Fungsionalitas utama ini diverifikasi melalui antarmuka Swagger/OpenAPI. Pengujian difokuskan pada skenario nyata di mana seorang *Student* melihat daftar kursus, lalu mendaftarkan dirinya ke salah satu kursus tersebut.

**Bukti Pengujian yang Dibutuhkan (Screenshots):**
- ![course-list](assets/course-list.png)
hasil `GET /api/v1/protected/courses` yang menampilkan daftar kursus. 
- ![enrollment-success](assets/enrollment-success.png)
hasil `POST /api/v1/protected/enrollments` saat Student berhasil mendaftar kursus.

#### 7. Swagger/OpenAPI dapat diakses (2 Poin)
**Deskripsi Implementasi:**
Dokumentasi API interaktif (*Interactive API Documentation*) dirender secara otomatis integrasi dari framework `django-ninja` yang sepenuhnya mendukung standar *OpenAPI*. Kehadiran Swagger UI ini menjadi sarana vital untuk mempermudah pemahaman skema antarmuka, format JSON (baik *request* maupun *response*), dan keperluan *testing* manual tanpa memerlukan aplikasi pihak ketiga seperti Postman.

**Pembuktian Akses Swagger:**
Halaman Swagger UI dapat langsung dibuka dan diuji coba dengan mengakses rute `/api/v1/docs` dan `/api/v1/protected/docs` melalui *browser*.

**Bukti Pengujian yang Dibutuhkan (Screenshots):**
- ![Swagger UI](assets/swagger-ui.png)
halaman Swagger UI yang memuat daftar berbagai endpoint API dari project LMS.

---

## 2. Fitur Tambahan: Paket 1 – LMS Experience (51 Poin)

| Status | Item Fitur Tambahan | Poin | Catatan / Link Dokumentasi |
| :---: | :--- | :---: | :--- |
| [x] | Tahap 1: Database & Model Enhancement (Section, Review, Wishlist) | - | Fondasi |
| [ ] | Search, filter, dan sorting course lanjutan | 12 | Tahap 2 |
| [ ] | Rating, review, dan wishlist course | 12 | Tahap 3 |
| [ ] | Curriculum dan progress belajar detail | 15 | Tahap 4 |
| [ ] | Student dashboard | 12 | Tahap 5 |

---

### Penjelasan Fitur Tambahan (Paket 1)

### Penjelasan Fitur Tambahan (Paket 1)

#### 1. Search, filter, dan sorting course lanjutan (12 Poin)
**Deskripsi Implementasi:**
*Course mudah ditemukan berdasarkan keyword, category, instructor, level, status, dan sorting.* Kami mengimplementasikan logika penyaringan menggunakan antarmuka `django-ninja` (Schema Filter) dikombinasikan dengan pencarian teks penuh via objek `Q` pada ORM Django di dalam *endpoint* `/courses`.

**Bukti Pengujian (Screenshots):**
- ![Search Field Filter Swagger](assets/swagger-filter-search.png)
- ![Filter Swagger](assets/swagger-filter.png)
pengujian endpoint GET /courses dengan memberikan input di parameter level/status pada Swagger

#### 2. Rating, review, dan wishlist course (12 Poin)
**Deskripsi Implementasi:**
*Student dapat memberi review dan menyimpan course favorit.* Fitur ini direalisasikan melalui model baru `Review` dan `Wishlist` yang terintegrasi di skema database, beserta pembuatan *endpoint* khusus (POST & GET) agar siswa dapat memanipulasi datanya.

**Bukti Pengujian (Screenshots):**
- ![Review Course Swagger](assets/swagger-review.png)
- ![Wishlist Course Swagger](assets/swagger-wishlist.png)

#### 3. Curriculum dan progress belajar detail (15 Poin)
**Deskripsi Implementasi:**
*Course punya section/module dan progress dihitung lebih akurat.* Struktur hierarki kursus kini dipecah menjadi `Course -> Section -> Lesson`. Penghitungan progres kelulusan (*completion*) dilakukan secara matematis pada *backend* sehingga nilainya lebih akurat.

**Bukti Pengujian (Screenshots):**
- ![Nested Curriculum Swagger](assets/swagger-curriculum.png)

#### 4. Student dashboard (12 Poin)
**Deskripsi Implementasi:**
*Ringkasan course aktif, progress, dan rekomendasi.* Endpoint `/dashboard/student` diciptakan secara eksklusif untuk merekapitulasi seluruh perjalanan belajar siswa secara *real-time*.

**Bukti Pengujian (Screenshots):**
- ![Student Dashboard Swagger](assets/swagger-dashboard.png)
