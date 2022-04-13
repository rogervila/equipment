from sqlalchemy_model_faker import factory
from equipment.framework.Database.AbstractSeeder import AbstractSeeder
from app.Models.Product import Product


class ProductSeeder(AbstractSeeder):
    def seed(self) -> None:
        product = factory(Product).make()

        with self.app.sql().session() as session:
            session.add(product)
            session.commit()

            # print(session.query(Product).count())
