from pathlib import Path
import pandas as pd
import re

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_FILE = BASE_DIR / "data" / "source" / "Online Retail.csv"
RAW_DIR = BASE_DIR / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)


def get_next_week_number(raw_dir: Path) -> int:
    existing_files = list(raw_dir.glob("raw_week_*.csv"))
    week_numbers = []

    for file in existing_files:
        match = re.search(r"raw_week_(\d+)\.csv", file.name)
        if match:
            week_numbers.append(int(match.group(1)))

    if not week_numbers:
        return 1

    return max(week_numbers) + 1


def load_dataset() -> pd.DataFrame:
    if not SOURCE_FILE.exists():
        raise FileNotFoundError(f"Source file not found: {SOURCE_FILE}")

    df = pd.read_csv(SOURCE_FILE, encoding="ISO-8859-1")

    if "InvoiceDate" not in df.columns:
        raise ValueError("Column 'InvoiceDate' not found in dataset.")

    # Parse tanggal dengan mode aman
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

    # Hapus baris yang gagal diparse
    df = df.dropna(subset=["InvoiceDate"])

    if df.empty:
        raise ValueError("Semua nilai InvoiceDate gagal diparse. Cek format tanggal pada file sumber.")

    # Urutkan berdasarkan waktu
    df = df.sort_values("InvoiceDate").reset_index(drop=True)

    return df


def ingest_next_week():
    df = load_dataset()

    min_date = df["InvoiceDate"].min().normalize()
    max_date = df["InvoiceDate"].max().normalize()

    next_week = get_next_week_number(RAW_DIR)

    start_date = min_date + pd.Timedelta(weeks=next_week - 1)
    end_date = start_date + pd.Timedelta(weeks=1)

    if start_date > max_date:
        print("Semua batch mingguan sudah di-ingest.")
        return

    batch_df = df[
        (df["InvoiceDate"] >= start_date) &
        (df["InvoiceDate"] < end_date)
    ].copy()

    if batch_df.empty:
        print(f"Tidak ada data untuk week {next_week} ({start_date.date()} - {end_date.date()}).")
        return

    output_file = RAW_DIR / f"raw_week_{next_week:02d}.csv"
    batch_df.to_csv(output_file, index=False)

    print(f"Berhasil ingest batch minggu ke-{next_week}")
    print(f"Periode: {start_date.date()} sampai {end_date.date()}")
    print(f"Jumlah baris: {len(batch_df)}")
    print(f"Tersimpan di: {output_file}")


if __name__ == "__main__":
    ingest_next_week()