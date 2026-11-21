
import hashlib
import secrets

from core.storage import StorageManager
from core.models import User, Product
from core.validation import DataValidator, ValidationError
from core.algorithms import SearchSortEngine


class UserService:

    def __init__(self):
        self.storage = StorageManager()

    @staticmethod
    def hash_password(password):
        salt = secrets.token_hex(16)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            600000
        ).hex()

        return f"{salt}${password_hash}"

    @staticmethod
    def verify_password(password, stored_password):
        try:
            salt, saved_hash = stored_password.split("$")

            password_hash = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt.encode("utf-8"),
                600000
            ).hex()

            return secrets.compare_digest(
                password_hash,
                saved_hash
            )

        except ValueError:
            return False

    def get_all_users(self):
        return self.storage.read_all("users.csv")

    def find_by_username(self, username):
        users = self.get_all_users()

        for user in users:
            if user["username"].lower() == username.lower():
                return user

        return None

    def register_user(self, user):
        DataValidator.validate_user(user)

        existing_user = self.find_by_username(user.username)

        if existing_user:
            raise ValidationError(
                "Username sudah digunakan."
            )

        user_data = user.to_dict()

        user_data["password"] = self.hash_password(
            user.password
        )

        self.storage.append("users.csv", user_data)

        return True

    def login(self, username, password):
        user = self.find_by_username(username)

        if user is None:
            return None

        if user["status"] != "Active":
            return None

        if not self.verify_password(
            password,
            user["password"]
        ):
            return None

        return user


class ProductService:

    def __init__(self):
        self.storage = StorageManager()

    def get_all_products(self):
        return self.storage.read_all("products.csv")

    def get_available_products(self):
        products = self.get_all_products()

        return [
            product for product in products
            if product["status"] == "Available"
            and int(product["stock"]) > 0
        ]

    def get_products_by_seller(self, seller_id):
        products = self.get_all_products()

        return [
            product for product in products
            if product["seller_id"] == seller_id
        ]

    def find_product(self, product_id):
        products = self.get_all_products()

        for product in products:
            if product["product_id"] == product_id:
                return product

        return None

    def add_product(self, product):
        DataValidator.validate_product(product)

        if self.find_product(product.product_id):
            raise ValidationError(
                "ID produk sudah digunakan."
            )

        product_data = product.to_dict()

        self.storage.append(
            "products.csv",
            product_data
        )

        return True

    def update_product(self, product_id, updates):
        product = self.find_product(product_id)

        if product is None:
            return False

        allowed_fields = [
            "product_name", "category", "brand",
            "size", "condition", "description",
            "price", "stock", "status", "image_path"
        ]

        for field in updates:
            if field not in allowed_fields:
                raise ValidationError(
                    f"Kolom {field} tidak boleh diubah."
                )

        updated_data = product.copy()
        updated_data.update(updates)

        updated_product = Product(
            product_id=updated_data["product_id"],
            seller_id=updated_data["seller_id"],
            product_name=updated_data["product_name"],
            category=updated_data["category"],
            brand=updated_data["brand"],
            size=updated_data["size"],
            condition=updated_data["condition"],
            description=updated_data["description"],
            price=int(updated_data["price"]),
            stock=int(updated_data["stock"]),
            status=updated_data["status"],
            image_path=updated_data["image_path"]
        )

        DataValidator.validate_product(updated_product)

        return self.storage.update(
            "products.csv",
            "product_id",
            product_id,
            updated_data
        )

    def delete_product(self, product_id):
        return self.storage.delete(
            "products.csv",
            "product_id",
            product_id
        )

    def search_products(self, keyword):
        products = self.get_available_products()

        keyword = keyword.lower()

        return [
            product for product in products
            if keyword in product["product_name"].lower()
            or keyword in product["brand"].lower()
        ]

    def sort_products_by_price(self, reverse=False):
        products = self.get_available_products()

        for product in products:
            product["price"] = int(product["price"])

        return SearchSortEngine.merge_sort(
            products,
            "price",
            reverse
        )
