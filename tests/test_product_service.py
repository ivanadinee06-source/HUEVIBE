
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.models import Product
from core.services import ProductService
from core.storage import StorageManager


class TestProductService:

    def __init__(self):
        StorageManager(data_dir="tests/test_data")
        self.service = ProductService.__new__(ProductService)
        self.service.storage = StorageManager(
            data_dir="tests/test_data"
        )

    def test_add_product(self):
        product = Product(
            "PRD001",
            "SEL001",
            "Oversized Shirt",
            "Clothing",
            "Local Brand",
            "L",
            "Good",
            "Kondisi masih bagus",
            65000,
            5
        )

        result = self.service.add_product(product)

        print("Tambah produk:", result)

    def test_get_all_products(self):
        products = self.service.get_all_products()

        print("Jumlah produk:", len(products))

    def test_search_products(self):
        products = self.service.search_products("Oversized")

        print("Hasil pencarian:", len(products))

    def test_update_product(self):
        result = self.service.update_product(
            "PRD001",
            {"price": 55000}
        )

        print("Ubah produk:", result)

    def test_sort_products(self):
        products = self.service.sort_products_by_price()

        print("Urutan harga:")
        for product in products:
            print(product["product_name"], product["price"])

    def test_delete_product(self):
        result = self.service.delete_product("PRD001")

        print("Hapus produk:", result)


if __name__ == "__main__":
    test = TestProductService()

    test.test_add_product()
    test.test_get_all_products()
    test.test_search_products()
    test.test_update_product()
    test.test_sort_products()
    test.test_delete_product()
