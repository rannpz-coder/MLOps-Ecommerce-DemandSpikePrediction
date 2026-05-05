from pathlib import Path
import pandas as pd
import re

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Hapus duplikat
    df = df.drop_duplicates()

    # Kolom penting
    important_cols = ["InvoiceDate", "StockCode", "Quantity", "UnitPrice"]
    existing_cols = [col for col in important_cols if col in df.columns]

    # Hapus missing value pada kolom penting
    df = df.dropna(subset=existing_cols)

    # Konversi tipe data
    if "InvoiceDate" in df.columns:
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

    if "Quantity" in df.columns:
        df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")

    if "UnitPrice" in df.columns:
        df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")

    # Hapus lagi jika hasil konversi gagal
    recheck_cols = ["InvoiceDate", "Quantity", "UnitPrice"]
    existing_recheck_cols = [col for col in recheck_cols if col in df.columns]
    df = df.dropna(subset=existing_recheck_cols)

    # Validasi nilai
    if "Quantity" in df.columns:
        df = df[df["Quantity"] > 0]

    if "UnitPrice" in df.columns:
        df = df[df["UnitPrice"] > 0]

    df = df.reset_index(drop=True)
    return df


def preprocess_all_raw_files():
    raw_files = sorted(RAW_DIR.glob("raw_week_*.csv"))

    if not raw_files:
        print("Belum ada file raw untuk diproses.")
        return

    for raw_file in raw_files:
        match = re.search(r"raw_week_(\d+)\.csv", raw_file.name)
        if not match:
            continue

        week_num = match.group(1)
        output_file = PROCESSED_DIR / f"clean_week_{week_num}.csv"

        if output_file.exists():
            print(f"Skip week {week_num}, sudah ada.")
            continue

        df = pd.read_csv(raw_file)
        clean_df = clean_dataframe(df)
        clean_df.to_csv(output_file, index=False)

        print(f"Processed: {raw_file.name} → {output_file.name}")
        print(f"Jumlah baris setelah cleaning: {len(clean_df)}")


if __name__ == "__main__":
    preprocess_all_raw_files()