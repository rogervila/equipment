import unittest
from equipment.framework.tests.TestCase import TestCase
from equipment.framework import equipment


class EquipmentHelperTest(TestCase):
    def test_equipment_function(self):
        self.assertIsNotNone(
            equipment('equipment.framework.App.Container')
        )


if __name__ == '__main__':
    unittest.main()
