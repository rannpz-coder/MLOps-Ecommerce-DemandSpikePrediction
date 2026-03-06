# MLOps-Ecommerce-DemandSpikePrediction
Project Overview
Proyek ini bertujuan untuk membangun sistem machine learning yang dapat memprediksi lonjakan permintaan produk pada platform e-commerce. Sistem dirancang menggunakan pendekatan MLOps sehingga model dapat diperbarui secara berkala ketika terjadi perubahan distribusi data.

Dataset yang digunakan adalah Online Retail Dataset dari UCI Machine Learning Repository yang berisi lebih dari 500.000 transaksi.

Machine learning task yang digunakan adalah binary classification:
- 0 = tidak terjadi lonjakan permintaan
- 1 = terjadi lonjakan permintaan

Model digunakan sebagai early warning system untuk membantu tim operasional dalam perencanaan stok dan manajemen supply chain.

## Repository Structure

data/
- raw : data mentah
- processed : data hasil preprocessing

models/
- penyimpanan model hasil training

notebooks/
- eksperimen dan exploratory data analysis

src/
- kode training dan inference model

config/
- konfigurasi pipeline machine learning

.devcontainer/
- konfigurasi GitHub Codespaces environment

## Running the Project with GitHub Codespaces

1. Buka repository ini di GitHub
2. Klik tombol **Code**
3. Pilih tab **Codespaces**
4. Klik **Create codespace on main**

Environment akan otomatis menyiapkan Python environment dan menginstall dependency dari file `requirements.txt`.

## Branching Strategy

Proyek ini menggunakan **GitHub Flow**.

Eksperimen awal dilakukan pada branch:
