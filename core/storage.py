
import csv
from pathlib import Path


class StorageError(Exception):
    """Exception khusus untuk kesalahan penyimpanan data."""


class StorageManager:
    """Mengelola proses baca dan tulis data CSV HUEVIBE."""

    CSV_HEADERS = {
        "users.csv": [
            "user_id", "username", "password", "full_name",
            "email", "phone", "address", "role", "status"
        ],
        "products.csv": [
            "product_id", "seller_id", "product_name", "category",
            "brand", "size", "condition", "description", "price",
            "stock", "status", "image_path"
        ],
        "carts.csv": [
            "cart_id", "buyer_id", "product_id", "quantity"
        ],
        "transactions.csv": [
            "transaction_id", "checkout_id", "buyer_id", "seller_id",
            "order_date", "total_amount", "shipping_address",
            "order_status"
        ],
        "transaction_details.csv": [
            "detail_id", "transaction_id", "product_id",
            "product_name", "quantity", "price", "subtotal"
        ],
        "payments.csv": [
            "payment_id", "checkout_id", "payment_method",
            "payment_date", "amount", "payment_status"
        ]
    }

    def __init__(self, data_dir=None):
        """Menentukan lokasi penyimpanan data."""
        if data_dir is None:
            project_dir = Path(__file__).resolve().parent.parent
            self.data_dir = project_dir / "data"
        else:
            self.data_dir = Path(data_dir)

        self.ensure_files()

    def ensure_files(self):
        """Membuat folder dan file CSV jika belum tersedia."""
        try:
            self.data_dir.mkdir(parents=True, exist_ok=True)

            for filename, headers in self.CSV_HEADERS.items():
                file_path = self.data_dir / filename

                if not file_path.exists() or file_path.stat().st_size == 0:
                    with open(
                        file_path,
                        mode="w",
                        newline="",
                        encoding="utf-8"
                    ) as file:
                        writer = csv.writer(file)
                        writer.writerow(headers)

        except OSError as error:
            raise StorageError(
                f"Gagal membuat file CSV: {error}"
            ) from error

    def read_all(self, filename):
        """Membaca seluruh data dari file CSV."""
        if filename not in self.CSV_HEADERS:
            raise ValueError("Nama file CSV tidak dikenal.")

        self.ensure_files()
        file_path = self.data_dir / filename

        try:
            with open(
                file_path,
                mode="r",
                newline="",
                encoding="utf-8"
            ) as file:
                reader = csv.DictReader(file)
                return list(reader)

        except (OSError, csv.Error, UnicodeError) as error:
            raise StorageError(
                f"Gagal membaca {filename}: {error}"
            ) from error

    def append(self, filename, data):
        """Menambahkan satu baris data ke file CSV."""
        if filename not in self.CSV_HEADERS:
            raise ValueError("Nama file CSV tidak dikenal.")

        self.ensure_files()
        file_path = self.data_dir / filename

        try:
            with open(
                file_path,
                mode="a",
                newline="",
                encoding="utf-8"
            ) as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=self.CSV_HEADERS[filename]
                )
                writer.writerow(data)

        except (OSError, csv.Error, ValueError) as error:
            raise StorageError(
                f"Gagal menambahkan data: {error}"
            ) from error

    def update(self, filename, key_column, key_value, updates):
        """Memperbarui data berdasarkan nilai kolom kunci."""
        rows = self.read_all(filename)

        if key_column not in self.CSV_HEADERS[filename]:
            raise ValueError("Kolom kunci tidak ditemukan.")

        found = False

        for row in rows:
            if row[key_column] == str(key_value):
                row.update(updates)
                found = True
                break

        if not found:
            return False

        self._write_rows(filename, rows)
        return True

    def delete(self, filename, key_column, key_value):
        """Menghapus data berdasarkan nilai kolom kunci."""
        rows = self.read_all(filename)

        if key_column not in self.CSV_HEADERS[filename]:
            raise ValueError("Kolom kunci tidak ditemukan.")

        filtered_rows = [
            row for row in rows
            if row[key_column] != str(key_value)
        ]

        if len(filtered_rows) == len(rows):
            return False

        self._write_rows(filename, filtered_rows)
        return True

    def _write_rows(self, filename, rows):
        """Menulis ulang seluruh data ke file CSV."""
        file_path = self.data_dir / filename

        try:
            with open(
                file_path,
                mode="w",
                newline="",
                encoding="utf-8"
            ) as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=self.CSV_HEADERS[filename]
                )
                writer.writeheader()
                writer.writerows(rows)

        except (OSError, csv.Error, ValueError) as error:
            raise StorageError(
                f"Gagal menyimpan perubahan: {error}"
            ) from error
