
from dataclasses import dataclass, asdict


@dataclass
class User:

    user_id: str
    username: str
    password: str
    full_name: str
    email: str
    phone: str
    address: str
    role: str
    status: str = "Active"

    def to_dict(self):
        return asdict(self)


@dataclass
class Product:

    product_id: str
    seller_id: str
    product_name: str
    category: str
    brand: str
    size: str
    condition: str
    description: str
    price: int
    stock: int
    status: str = "Available"
    image_path: str = ""

    def to_dict(self):
        return asdict(self)


@dataclass
class Transaction:

    transaction_id: str
    checkout_id: str
    buyer_id: str
    seller_id: str
    order_date: str
    total_amount: int
    shipping_address: str
    order_status: str = "Menunggu Konfirmasi"

    def to_dict(self):
        return asdict(self)
