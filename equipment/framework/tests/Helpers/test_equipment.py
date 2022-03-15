import unittest
from equipment.framework.tests.BaseTest import BaseTest
from equipment.framework import Equipment


class test_equipment(BaseTest):
    def test_equipment_function(self):
        self.assertIsNotNone(
            Equipment('equipment.framework.App.Container')
        )


if __name__ == '__main__':
    unittest.main()
