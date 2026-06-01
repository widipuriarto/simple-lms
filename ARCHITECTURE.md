# Dokumentasi Arsitektur Advanced API LMS

## 1. Diagram Arsitektur (Mermaid)
```mermaid
graph TD
    Client[Client / Student / Admin] -->|HTTP Request| API[Django Ninja API]
    
    API <-->|Read/Write (Relational Data)| DB[(PostgreSQL)]
    API <-->|Write Logs / Read Analytics| Mongo[(MongoDB)]
    
    API <-->|Check/Set Cache & Rate Limit| Redis[(Redis)]
    
    API -->|Send Async Task| RMQ[RabbitMQ]
    RMQ -->|Consume Task| Worker[Celery Worker]
    Beat[Celery Beat] -->|Schedule Task| RMQ
    Worker -->|Read/Write Result| Redis
```

## 2. Caching Strategy & Rate Limiting
- **Caching**: Menggunakan Redis sebagai backend *cache*. Data yang berat saat ditarik dari PostgreSQL (seperti `list_courses`) disimpan di memori Redis dengan *timeout* 15 menit agar pencarian selanjutnya sangat instan.
- **Cache Invalidation**: Saat data *course* diubah (Update) atau dihapus (Delete), API akan menjalankan `cache.clear()` dan `cache.delete()` untuk menghapus cache yang sudah usang, memastikan data selalu sinkron.
- **Rate Limiting**: Menggunakan arsitektur *Sliding Window* pada Redis. API menyimpan array *timestamp* untuk tiap alamat IP. Jika mendeteksi lebih dari 60 *request* dalam 60 detik terakhir, API mengembalikan error HTTP 429 (Too Many Requests).

## 3. Asynchronous Task Flow
1. API menerima *request* dari pengguna (misal: Enroll Course).
2. API menjalankan `.delay()` pada *task* Celery.
3. *Task* diubah menjadi pesan (*message*) dan dilempar ke antrean **RabbitMQ**.
4. API langsung memberikan respons sukses ke pengguna tanpa membuat loading lama.
5. **Celery Worker** yang siaga akan mengambil pesan tersebut dari RabbitMQ dan mengeksekusinya (misal: simulasi kirim email) di latar belakang (background).

## 4. Redis CLI Commands Documentation
Perintah dasar untuk memonitor Redis di Docker:
- `docker exec -it redis redis-cli` (Masuk ke Redis console)
- `PING` (Tes koneksi, respons: PONG)
- `KEYS *` (Melihat semua kunci yang sedang di-cache)
- `FLUSHALL` (Mereset dan mengosongkan seluruh memori Redis)
