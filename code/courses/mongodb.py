import pymongo
from django.conf import settings
from datetime import datetime

# 1. Membuka koneksi ke MongoDB menggunakan URI yang sudah kita set di settings.py
client = pymongo.MongoClient(settings.MONGO_URI)

# 2. Memilih database (dalam hal ini 'lms_analytics')
db = client[settings.MONGO_DB_NAME]

def log_activity(user_id: int, action: str, details: dict = None):
    """
    Fungsi bantuan untuk mencatat aktivitas pengguna ke MongoDB.
    """
    if details is None:
        details = {}
        
    # Membentuk struktur dokumen (seperti JSON)
    log_entry = {
        "user_id": user_id,
        "action": action,
        "details": details,
        "timestamp": datetime.utcnow()
    }
    
    # 3. Menyimpan dokumen ke dalam koleksi 'activity_logs'
    db.activity_logs.insert_one(log_entry)

def get_activity_report():
    """
    Menggunakan fitur 'Aggregation Pipeline' dari MongoDB untuk 
    menghitung total dari masing-masing aksi (misal: berapa banyak total ENROLL).
    """
    pipeline = [
        # Tahap 1: Mengelompokkan data berdasarkan field 'action'
        {
            "$group": {
                "_id": "$action", 
                "total_count": {"$sum": 1} # Hitung jumlah kemunculannya
            }
        },
        # Tahap 2: Mengurutkan dari jumlah yang terbanyak
        {
            "$sort": {"total_count": -1}
        }
    ]
    
    # Menjalankan fungsi agregasi pada koleksi activity_logs
    results = list(db.activity_logs.aggregate(pipeline))
    
    # Merapikan format output agar mudah dibaca oleh Frontend/Mobile
    report = {}
    for r in results:
        action_name = r["_id"]
        report[action_name] = r["total_count"]
        
    return report
