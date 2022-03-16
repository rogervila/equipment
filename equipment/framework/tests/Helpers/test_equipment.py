import unittest
from equipment.framework.tests.BaseTest import BaseTest
from equipment.framework import equipment


class test_equipment(BaseTest):
    def test_equipment_function(self):
        self.assertIsNotNone(
            equipment('equipment.framework.App.Container')
        )


if __name__ == '__main__':
    unittest.main()
