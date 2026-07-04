# Simple LMS Backend (Extended)

Simple LMS adalah sebuah sistem manajemen pembelajaran berarsitektur *microservices-ready* yang dibangun di atas fondasi Django Ninja. Proyek ini merupakan pengembangan tingkat lanjut yang mencakup fitur-fitur "LMS Experience" mutakhir seperti hierarki kurikulum (*Section & Lesson*), ulasan (*review*), daftar keinginan (*wishlist*), hingga dasbor interaktif siswa.

Seluruh infrastruktur telah diorkestrasi secara penuh menggunakan Docker, yang mencakup pengolahan basis data relasional, antrean pesan (*message broker*), hingga *caching* tingkat tinggi.

## 🏗️ Arsitektur Infrastruktur (Docker Compose)
Proyek ini mengandalkan 8 layanan utama yang saling terhubung:
1. **web**: Server utama Django yang mengekspos API di port `8000`.
2. **db**: PostgreSQL 15 sebagai basis data relasional utama.
3. **redis**: Redis 7 untuk sistem *caching* API (menyimpan hasil kueri kompleks).
4. **mongodb**: MongoDB 7 untuk pencatatan *log* aktivitas pengguna (*NoSQL*).
5. **rabbitmq**: RabbitMQ 3 sebagai *Message Broker* untuk pengolahan antrean tugas asinkron.
6. **celery-worker**: Pekerja asinkron untuk mengeksekusi tugas berat di latar belakang.
7. **celery-beat**: Penjadwal (*scheduler*) untuk tugas-tugas rutin.
8. **flower**: Dasbor pemantauan (*monitoring*) antrean Celery di port `5555`.

---

## 🚀 Cara Menjalankan Proyek

1. **Persiapan Environtment**
   Pastikan Docker dan Docker Compose telah terpasang di sistem Anda.
   ```bash
   cp .env.example .env
   ```

2. **Jalankan Orkestrasi Docker**
   Perintah ini akan membangun *image* dan menjalankan seluruh *container* di latar belakang:
   ```bash
   docker-compose up -d --build
   ```

3. **Bibitkan Data (Seeding)**
   Jika ini pertama kalinya Anda menjalankan proyek ini, wajib memasukkan data percontohan agar seluruh fitur (khususnya *Dashboard*) dapat berfungsi secara maksimal:
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py seed
   ```

4. **Akses Layanan**
   - **API (Swagger UI):** [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
   - **Django Admin:** [http://localhost:8000/admin](http://localhost:8000/admin)
   - **Celery Flower:** [http://localhost:5555](http://localhost:5555)

---

## 🔐 Akun Demo (Seeding Data)

Skrip `seed.py` secara otomatis menciptakan ribuan data acak beserta kredensial berikut untuk keperluan pengujian. Terdapat dua mode pengguna utama:

| Peran | Username | Password | Deskripsi |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `password123` | Akses penuh Django Admin dan sistem keseluruhan. |
| **Instructor** | `instructor` | `123` | Pengajar dengan beberapa kursus fiktif. |
| **Student** | `student` | `123` | Siswa reguler dengan data *progress*, *enrollment*, *review*, dan *wishlist*. |

*(Catatan Tambahan: Tersedia juga akun `student0` hingga `student14` serta `instructor0` hingga `instructor4` dengan sandi `password123` jika dibutuhkan).*

---

## 📡 Endpoint Utama API (LMS Experience)

Keseluruhan *endpoint* dilindungi oleh *JSON Web Token* (JWT). Dapatkan Token Anda di rute `POST /api/v1/auth/token` terlebih dahulu.

| Endpoint | Method | Role | Keterangan |
| :--- | :---: | :---: | :--- |
| `/api/v1/protected/courses` | `GET` | All | Pencarian dan penyaringan kursus (*search, level, status*). |
| `/api/v1/protected/courses/{id}` | `GET` | All | Detail kursus, mencakup kurikulum berjenjang (*Section & Lesson*). |
| `/api/v1/protected/courses/{id}/reviews`| `GET, POST` | All | Membaca dan membuat *Rating/Review* (Siswa wajib mendaftar/*enroll* dulu). |
| `/api/v1/protected/wishlist/{course_id}` | `POST` | Student | Memasukkan atau mengeluarkan kursus dari daftar favorit. |
| `/api/v1/protected/wishlist` | `GET` | Student | Melihat daftar keseluruhan kursus di dalam *wishlist*. |
| `/api/v1/protected/courses/{id}/progress`| `GET` | Student | Menghitung persentase progres belajar secara presisi. |
| `/api/v1/protected/dashboard/student` | `GET` | Student | Merekap kursus aktif, tamat, dan rekomendasi (*Dashboard*). |

> **Catatan Dokumentasi Proyek:**
> Untuk melihat bukti visual (*screenshot*) pengujian per fitur dan detail deskripsi implementasi arsitektur komponen wajib serta paket lanjutan, silakan merujuk secara khusus ke file [Dokumentasi_Fitur.md](Dokumentasi_Fitur.md).