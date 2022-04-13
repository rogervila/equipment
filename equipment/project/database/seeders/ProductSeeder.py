from sqlalchemy_model_faker import factory
from equipment.framework.Database.AbstractSeeder import AbstractSeeder
from app.Models.Product import Product


class ProductSeeder(AbstractSeeder):
    @staticmethod
    def seed() -> None:
        product = factory(Product).make()
        print(product)
