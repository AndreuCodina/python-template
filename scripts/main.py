from decimal import Decimal

from domain.entities.product import Product


def main() -> None:
    Product(name="Sample Product", price=Decimal("19.99"), is_discontinued=False)


if __name__ == "__main__":
    main()
