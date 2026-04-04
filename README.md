# MLOps Ecommerce Demand Spike Prediction

## Deskripsi Proyek
Proyek ini bertujuan untuk mengimplementasikan pipeline data ingestion dan preprocessing dalam konteks Machine Learning Operations (MLOps).

Dataset yang digunakan adalah **Online Retail Dataset**, yang diperlakukan sebagai data dinamis melalui mekanisme **weekly ingestion** berdasarkan kolom `InvoiceDate`.

Pipeline ini dirancang untuk mendukung konsep **Continual Learning**, di mana data terus bertambah dan diproses secara bertahap.

---

## Struktur Folder
```bash
.
├── data
│   ├── source
│   │   └── Online Retail.csv
│   ├── raw
│   │   ├── raw_week_01.csv
│   │   ├── raw_week_02.csv
│   │   └── raw_week_03.csv
│   └── processed
│       ├── clean_week_01.csv
│       ├── clean_week_02.csv
│       └── clean_week_03.csv
├── src
│   ├── ingest_data.py
│   ├── preprocess.py
│   ├── train.py
│   └── predict.py
├── requirements.txt
└── README.md
