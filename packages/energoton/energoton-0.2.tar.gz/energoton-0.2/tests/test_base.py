import unittest

from energoton.base import Id


class TestId(unittest.TestCase):
    def test_id_generated(self):
        unit1 = Id()
        unit2 = Id()

        self.assertNotEqual(unit1.id, unit2.id)

    def test_id_equality(self):
        unit1 = Id()
        unit2 = Id()

        self.assertNotEqual(unit1, unit2)

        unit2 = Id(unit1.id)
        self.assertEqual(unit1, unit2)
