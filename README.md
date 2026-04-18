## Data Versioning (DVC)

Proyek ini menggunakan DVC untuk melacak perubahan dataset tanpa membebani repositori Git.

### Alur Versioning Data
1. Inisialisasi DVC menggunakan `dvc init`
2. Tracking dataset awal menggunakan `dvc add`
3. Menjalankan ingestion untuk menghasilkan data baru
4. Tracking dataset baru dengan `dvc add`
5. Melihat perubahan versi menggunakan `dvc diff`

### Contoh Perintah
```bash
dvc add data/raw/raw_week_03.csv
python src/ingest_data.py
dvc add data/raw/raw_week_04.csv
dvc diff HEAD~1 HEAD


