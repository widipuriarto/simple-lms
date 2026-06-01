import time
from celery import shared_task
from django.core.cache import cache

# Task 1: Kirim Email (Asinkron)
@shared_task
def send_enrollment_email(user_email: str, course_title: str):
    """
    Simulasi mengirim email saat student berhasil enroll.
    """
    print(f"[CELERY] Mengirim email ke {user_email} untuk course '{course_title}'...")
    time.sleep(3) # Simulasi proses email yang berjalan lambat (3 detik)
    print("[CELERY] Email berhasil dikirim!")
    return True

# Task 2: Buat Sertifikat (Asinkron)
@shared_task
def generate_certificate(user_name: str, course_title: str):
    """
    Simulasi pembuatan sertifikat PDF saat course selesai.
    """
    print(f"[CELERY] Mulai membuat sertifikat PDF untuk {user_name}...")
    time.sleep(5) # Simulasi proses memakan waktu 5 detik
    print("[CELERY] Sertifikat berhasil dibuat!")
    return f"/media/certificates/{user_name.replace(' ', '_')}.pdf"

# Task 3: Export Laporan CSV (Asinkron)
@shared_task
def export_course_report(admin_email: str):
    """
    Simulasi ekspor data massal ke CSV yang berjalan di latar belakang.
    """
    print(f"[CELERY] Mengekspor laporan CSV. Akan dikirim ke {admin_email}...")
    time.sleep(10) # Simulasi proses ekspor yang sangat lambat (10 detik)
    print("[CELERY] Laporan CSV siap!")
    return True

# Task 4: Update Statistik secara Berkala (Scheduled / Cron Job)
@shared_task
def update_course_statistics():
    """
    Task ini nantinya akan dijadwalkan secara otomatis oleh Celery Beat.
    """
    print("[CELERY] Menghitung ulang statistik enrollment untuk semua course...")
    time.sleep(2)
    cache.set("global_course_stats_updated", time.time())
    print("[CELERY] Statistik berhasil diupdate!")
    return True
