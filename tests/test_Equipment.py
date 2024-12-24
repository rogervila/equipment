import unittest
from dependency_injector.containers import DynamicContainer
from equipment import Equipment, equipment
from equipment.Log.LoggerFactory import LoggerFactory
from equipment.Queue.QueueFactory import QueueFactory
from equipment.Storage.StorageFactory import StorageFactory
from equipment.Database.SQLAlchemyFactory import SQLAlchemyFactory
from runtype import isa

TEST_CONFIG = {
    "app": {
        "name": "test",
        "env": "testing",
    },
    "log": {
        "level": "DEBUG",
        "channel": None,
        "formatter": None,
    },
    "storage": {
        "disk": "local",
        "disks": {
            "local": {
                "path": "storage"
            }
        }
    },
    "queue": {
        "connection": "sync",
        "connections": {
            "sync"
        }
    },
    "database": {
        "connection": "sqlite",
        "connections": {
            "sqlite": {
                "schema": "sqlite",
                "database": ":memory:",
            }
        }
    }
}


class EquipmentTest(unittest.TestCase):
    def test_equipment_method(self):
        instance = equipment()
        self.assertTrue(isa(instance, DynamicContainer))

    def test_default_singletons(self):
        instance = Equipment()

        instance.config.from_dict(TEST_CONFIG)

        self.assertTrue(isa(instance.log(), LoggerFactory))
        self.assertTrue(isa(instance.storage(), StorageFactory))
        self.assertTrue(isa(instance.queue(), QueueFactory))
        self.assertTrue(isa(instance.database(), SQLAlchemyFactory))


if __name__ == '__main__':
    unittest.main()
