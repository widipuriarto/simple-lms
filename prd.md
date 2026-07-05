# Product Requirements Document (PRD)
**Project Name:** Simple LMS
**Date:** July 2026
**Version:** 1.0

---

## 1. Problem Statement
Seiring dengan meningkatnya kebutuhan akan pendidikan jarak jauh (*e-learning*), banyak lembaga dan kreator konten kesulitan menemukan platform LMS yang gratis, *open-source*, fleksibel, namun tetap aman. Mayoritas LMS terlalu kompleks (membingungkan pengguna) atau memiliki manajemen *role* (peran) yang lemah sehingga sulit memisahkan kewenangan antara siswa, pengajar, dan administrator. 

Selain itu, kendala performa sering terjadi pada LMS saat jumlah kursus membengkak. Kebutuhan akan adanya platform yang modern (responsif), memiliki pemrosesan latar belakang (*background tasks*), *caching* untuk kecepatan, dan antarmuka (UI) yang bersih namun lengkap sangatlah krusial untuk menyelesaikan tantangan ini.

## 2. Goals
Tujuan dari pengembangan Simple LMS adalah:
- **Membangun sistem *decoupled* yang andal:** Memisahkan Frontend (React) dan Backend (Django Ninja) untuk skalabilitas tinggi.
- **Menyediakan alur otorisasi multi-role yang ketat:** Menciptakan ekosistem terpadu untuk tiga jenis aktor: *Student*, *Instructor*, dan *Admin*.
- **Meningkatkan pengalaman interaktif:** Menerapkan sistem ulasan (Rating & Review), fitur Wishlist, dan Ruang Diskusi yang mudah digunakan.
- **Memastikan performa & keandalan tingkat tinggi:** Menerapkan Redis untuk *caching* data dan Celery/Redis untuk tugas-tugas berat (misalnya ekspor CSV) agar performa server tetap stabil.

## 3. Target User
Platform ini ditujukan untuk 3 kelompok pengguna utama:
1. **Student (Siswa):** Pelajar dari berbagai rentang usia yang ingin mendaftar ke kursus, melihat progres belajar secara visual, memberikan penilaian (rating), dan menyimpan daftar kelas favorit.
2. **Instructor (Pengajar):** Kreator konten, guru, atau dosen yang mempublikasikan ilmu mereka. Mereka membutuhkan alat yang sederhana untuk mendesain kurikulum, membuat materi kursus, dan mengelola kelas mereka sendiri.
3. **Admin (Administrator):** Pemilik *platform* atau staf moderasi yang bertugas menjaga keamanan dan kebersihan sistem. Admin fokus pada pembacaan metrik (*analytics*) dan moderasi konten ilegal (menghapus kursus / komentar nakal).

## 4. User Story
Berikut adalah cerita pengguna berdasarkan perannya:

### Sebagai Student:
- *Sebagai siswa*, saya ingin mencari kursus berdasarkan kata kunci, tingkat kesulitan, dan kategori agar saya dapat menemukan materi yang tepat.
- *Sebagai siswa*, saya ingin memasukkan kursus yang menarik ke dalam **Wishlist** agar bisa mendaftar di lain waktu.
- *Sebagai siswa*, saya ingin **Mendaftar (Enroll)** ke dalam kursus untuk mendapatkan akses materi.
- *Sebagai siswa*, saya ingin mencentang materi yang sudah saya baca sehingga persentase **Progres Belajar** saya meningkat.
- *Sebagai siswa*, saya ingin bertanya atau merespon pertanyaan di **Ruang Diskusi** agar dapat berinteraksi dengan orang lain.
- *Sebagai siswa*, saya ingin memberikan **Ulasan dan Bintang 1-5** pada kursus yang telah saya ambil untuk membantu calon siswa lain.

### Sebagai Instructor:
- *Sebagai instruktur*, saya ingin **Membuat (Create)** kursus baru dan merancang silabus (Section & Lesson).
- *Sebagai instruktur*, saya ingin dapat menyunting **(Edit)** judul dan deskripsi kursus milik saya sendiri kapanpun diperlukan.
- *Sebagai instruktur*, saya ingin melihat daftar katalog kursus yang telah saya rilis melalui *Instructor Dashboard*.

### Sebagai Admin:
- *Sebagai admin*, saya ingin melihat **Dashboard Analytics** (total siswa, kursus, pendaftaran) untuk mengevaluasi pertumbuhan *platform*.
- *Sebagai admin*, saya ingin menekan tombol **Hapus** pada kursus yang melanggar pedoman komunitas secara mutlak.
- *Sebagai admin*, saya ingin **menghapus komentar** toksik atau spam dari sistem diskusi.
- *Sebagai admin*, saya ingin mengunduh riwayat aktivitas *(Export Data)* ke dalam CSV tanpa membuat server macet lambat (via Celery).

## 5. Functional Requirements
Sistem harus mampu melakukan hal-hal berikut:

- **Autentikasi & Keamanan:**
  - Login berbasis JSON Web Token (JWT) yang diterbitkan melalui `POST /api/v1/auth/sign-in`.
  - Sistem Role-Based Access Control (RBAC) pada *backend* (menggunakan *decorator* `@role_required`) dan *frontend* (menggunakan `<ProtectedRoute>`).
- **Sistem Modul Kursus:**
  - Dukungan hierarki konten: `Course` -> `Section` -> `Lesson`.
  - API untuk pencarian (*search*) dan penyaringan (*filtering*) berbasis *query params*.
- **Student Engagement System:**
  - Fungsi klik tombol Enroll (`POST /enrollments`).
  - Fungsi klik tombol Tandai Selesai (`POST /enrollments/{id}/progress`).
  - Fungsi CRUD Ulasan dan Komentar.
- **Admin Moderation & Analytics:**
  - Agregasi data analitik pada backend yang di-*feed* ke dasbor frontend.
  - Otoritas absolut `DELETE /courses/{id}` dan `DELETE /comments/{id}` tanpa pembatasan hak kepemilikan.
  - Trigger *Celery Background Worker* untuk pengolahan komputasi berat.

## 6. Non-Functional Requirements
- **Performance:** Waktu *response* API untuk pembacaan katalog kursus harus berada di bawah 300ms. Ini dicapai dengan fitur Redis *Caching* pada `GET /courses`.
- **Security:** *Password* dalam *database* (SQLite/PostgreSQL) wajib disimpan dalam format *hash*. Serangan *Cross-Origin Resource Sharing* (CORS) dikelola menggunakan Vite Proxy selama *development*.
- **Usability (UI/UX):** Antarmuka wajib responsif (*mobile-friendly*), menggunakan desain kontemporer (*Slate Monochrome*), dengan indikator asinkron (*loading spinner*) di setiap pengambilan data (*API call*).
- **Maintainability:** Penggunaan arsitektur React *component-based* (Pemecahan per komponen/halaman) agar mudah dikembangkan (*scalable*).
- **Reliability:** Fungsi *Export* admin tidak boleh menunda *HTTP Response* sehingga harus didelegasikan kepada Celery (Tugas Paralel Asynchronous).

## 7. Scope (Ruang Lingkup)
- **In-Scope:**
  - Pembangunan 24 Endpoint REST API (Django Ninja).
  - Pembangunan Sistem Frontend End-to-End dengan React Router & TailwindCSS.
  - Implementasi RBAC (Admin, Instructor, Student).
  - Fitur Caching (Redis) dan Job Queue (Celery).
  - Fitur Diskusi, Ulasan, Wishlist, dan Kalkulasi Progres.
- **Out-of-Scope (Tidak Termasuk pada Versi 1.0):**
  - Gateway pembayaran (Payment Gateway) untuk kursus berbayar.
  - Integrasi kelas video langsung (Zoom/Google Meet/WebRTC).
  - Sistem ujian interaktif mandiri (Kuis Pilihan Ganda dengan penilaian waktu).
  - Gamifikasi kelas lanjut (seperti Sistem *Badges*, *Leaderboard*, XP).

## 8. System Design (UI/UX Architecture)
Untuk memberikan pengalaman pengguna yang sangat premium, eksklusif, dan intuitif, desain antarmuka platform ini akan direkayasa secara ketat mengikuti pedoman desain **Apple Ecosystem (Human Interface Guidelines)**.

### Karakteristik Ekosistem Desain Apple:
1. **Typography (Tipografi):**
   - Menggunakan rupa huruf *San-Serif* modern yang jernih dan beraksen geometri. Idealnya menggunakan keluarga *San Francisco (SF Pro)*, atau alternatif serumpun seperti **Inter** atau **Roboto** sebagai standardisasi web lintas platform.
   - Mengandalkan hierarki ketebalan font (*Font Weight*): *Extrabold* untuk *Headline/Title*, dan *Regular/Medium* untuk teks paragraf demi keterbacaan tingkat tinggi.
2. **Color Palette (Palet Warna):**
   - **Latar Belakang (Background):** Dominasi warna *Off-White* yang sangat lembut seperti **`#F5F5F7`** (mirip warna *casing* Mac/iPad putih) untuk *background* layar utama, dan *Pure White* **`#FFFFFF`** untuk *Surface/Card*.
   - **Teks (Foreground):** Teks utama tidak menggunakan hitam pekat, melainkan abu-abu gelap kehitaman seperti **`#1D1D1F`** (*slate-900*). Teks sekunder menggunakan warna abu-abu lembut (*slate-500*).
   - **Warna Aksen (Accent):** Biru khas Apple **`#0071E3`** (*blue-600*) digunakan untuk elemen interaktif (tombol primer, *link*, atau *checkbox* aktif) guna menonjolkan ajakan bertindak (*Call to Action*).
3. **Materials & Depth (Glassmorphism & Material):**
   - Penggunaan efek *frosted glass* (kaca buram) pada elemen mengambang seperti *Navbar*, *Dropdown*, atau *Modal*. Di Tailwind, efek ini dicapai menggunakan utilitas `backdrop-blur-md` dan `bg-white/80`.
   - Bayangan (*Drop Shadows*) yang digunakan bersifat sangat luas, *diffuse*, dan tipis (`shadow-sm` hingga `shadow-lg` dengan opasitas rendah) demi menciptakan sensasi kedalaman ruang (*depth*) tanpa terlihat berlebihan/norak.
4. **Border Radius (Sudut Melengkung):**
   - Karakteristik paling khas Apple adalah transisi sudut melengkung (*Squircle*). Seluruh *Card*, wadah, dan blok kontainer akan menggunakan `rounded-2xl` (16px) hingga `rounded-3xl` (24px).
   - Tombol-tombol (*Buttons*) dan *Chip/Badge* (kategori) akan menggunakan bentuk pil atau kapsul (*fully rounded* / `rounded-full`) untuk memberikan kesan luwes dan ramah.
5. **Whitespace & Layout (Ruang Kosong):**
   - Spasi antar elemen sangat lapang (*generous padding & margin*). Layout bernapas dan tidak sesak, fokus mutlak pada konten (kursus dan materi belajar) tanpa distraksi elemen UI yang tidak perlu (*Minimalism*).
