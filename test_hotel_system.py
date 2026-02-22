import os
import unittest
from hotel_system import HotelSystem


class TestHotelSystem(unittest.TestCase):

    def setUp(self):
        self.system = HotelSystem()
        for file in [
                "hotels.json",
                "customers.json",
                "reservations.json"]:
            if os.path.exists(file):
                os.remove(file)

    def test_hotel_creation(self):
        self.assertTrue(
            self.system.create_hotel(1, "Test", "NY", 10)
        )
        self.assertEqual(len(self.system.display_hotels()), 1)

    def test_duplicate_hotel(self):
        self.system.create_hotel(1, "Test", "NY", 10)
        self.assertFalse(
            self.system.create_hotel(1, "Test", "NY", 10)
        )

    def test_customer_creation(self):
        self.assertTrue(
            self.system.create_customer(
                1, "John", "john@mail.com", "123"
            )
        )

    def test_reservation_flow(self):
        self.system.create_hotel(1, "Test", "NY", 1)
        self.system.create_customer(
            1, "John", "john@mail.com", "123"
        )
        self.assertTrue(
            self.system.create_reservation(1, 1, 1)
        )
        self.assertEqual(
            len(self.system.display_reservations()), 1
        )
        self.assertTrue(
            self.system.cancel_reservation(1)
        )
        self.assertEqual(
            len(self.system.display_reservations()), 0
        )

    def test_invalid_reservation(self):
        self.assertFalse(
            self.system.create_reservation(1, 99, 99)
        )

    def test_modify_customer(self):
        self.system.create_customer(
            1, "John", "john@mail.com", "123"
        )
        self.assertTrue(
            self.system.modify_customer(1, name="Jane")
        )


if __name__ == "__main__":
    unittest.main()