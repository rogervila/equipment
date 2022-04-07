from equipment.framework.Database.AbstractSeeder import AbstractSeeder
from .ProductSeeder import ProductSeeder


class Seeder(AbstractSeeder):
    @staticmethod
    def seed() -> None:
        ProductSeeder.seed()
        # Add more seeders here
