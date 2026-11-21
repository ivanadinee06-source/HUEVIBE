
class ValidationError(Exception):
    pass


class DataValidator:

    VALID_ROLES = ["Admin", "Seller", "Buyer"]

    VALID_CATEGORIES = [
        "Clothing",
        "Footwear",
        "Bags",
        "Accessories"
    ]

    VALID_CONDITIONS = [
        "Like New",
        "Excellent",
        "Good",
        "Fair"
    ]

    VALID_PRODUCT_STATUS = [
        "Available",
        "Reserved",
        "Sold"
    ]

    VALID_ORDER_STATUS = [
        "Menunggu Konfirmasi",
        "Ditolak",
        "Menunggu Pembayaran",
        "Diproses",
        "Dikirim",
        "Selesai",
        "Dibatalkan"
    ]

    @staticmethod
    def validate_required(data, fields):
        for field in fields:
            value = data.get(field)

            if value is None or str(value).strip() == "":
                raise ValidationError(
                    f"{field} tidak boleh kosong."
                )

    @staticmethod
    def validate_user(user):
        data = user.to_dict()

        DataValidator.validate_required(
            data,
            ["user_id", "username", "password",
             "full_name", "email", "role"]
        )

        if data["role"] not in DataValidator.VALID_ROLES:
            raise ValidationError("Role pengguna tidak valid.")

        if "@" not in data["email"]:
            raise ValidationError("Format email tidak valid.")

        return True

    @staticmethod
    def validate_product(product):
        data = product.to_dict()

        DataValidator.validate_required(
            data,
            ["product_id", "seller_id", "product_name",
             "category", "condition", "description"]
        )

        if data["category"] not in DataValidator.VALID_CATEGORIES:
            raise ValidationError("Kategori produk tidak valid.")

        if data["condition"] not in DataValidator.VALID_CONDITIONS:
            raise ValidationError("Kondisi produk tidak valid.")

        if data["status"] not in DataValidator.VALID_PRODUCT_STATUS:
            raise ValidationError("Status produk tidak valid.")

        if not isinstance(data["price"], int) or data["price"] < 0:
            raise ValidationError(
                "Harga harus berupa bilangan bulat positif atau nol."
            )

        if not isinstance(data["stock"], int) or data["stock"] < 0:
            raise ValidationError(
                "Stok harus berupa bilangan bulat positif atau nol."
            )

        return True

    @staticmethod
    def validate_transaction(transaction):
        data = transaction.to_dict()

        DataValidator.validate_required(
            data,
            ["transaction_id", "checkout_id", "buyer_id",
             "seller_id", "order_date", "shipping_address"]
        )

        if data["order_status"] not in DataValidator.VALID_ORDER_STATUS:
            raise ValidationError("Status pesanan tidak valid.")

        if (
            not isinstance(data["total_amount"], int)
            or data["total_amount"] < 0
        ):
            raise ValidationError("Total transaksi tidak valid.")

        return True
