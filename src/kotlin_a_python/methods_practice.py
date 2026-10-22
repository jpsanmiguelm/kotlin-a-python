from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    id: str
    name: str
    price: float

    def is_expensive(self) -> bool:
        return self.price > 50

    def label(self) -> str:
        text = f"{self.name}: ${self.price}"
        if self.is_expensive():
            return f"{text} (expensive)"
        return text


@dataclass(frozen=True)
class ProductDTO:
    id: str
    name: str | None
    price_cents: int

    def to_domain(self) -> Product:
        return Product(
            id=self.id,
            name=self.name if self.name is not None else "Unnamed product",
            price=self.price_cents / 100,
        )


def main() -> None:
    dtos = [
        ProductDTO("1", "Protein", 4999),
        ProductDTO("2", None, 12000),
    ]

    products = [dto.to_domain() for dto in dtos]
    for p in products:
        print(p.label())


if __name__ == "__main__":
    main()
