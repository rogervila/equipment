from equipment.framework.Database.AbstractSeeder import AbstractSeeder
from .ProductSeeder import ProductSeeder


class Seeder(AbstractSeeder):
    def seed(self) -> None:
        ProductSeeder().seed()
        # Add more seeders here
