"""
Hotel Reservation System
Compliant with PEP8, unittest-ready, and resilient to invalid JSON data.
"""

import json
import os
from datetime import datetime
from typing import List, Dict


def load_data(filename: str) -> List[Dict]:
    """Load JSON data safely from file."""
    if not os.path.exists(filename):
        return []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {filename}. Resetting file.")
        return []
    except OSError as error:
        print(f"File error in {filename}: {error}")
        return []


def save_data(filename: str, data: List[Dict]) -> None:
    """Save data to JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except OSError as error:
        print(f"File write error in {filename}: {error}")


class Hotel:
    """Represents a hotel."""

    def __init__(self, hotel_id: int, name: str,
                 location: str, total_rooms: int) -> None:
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.total_rooms = total_rooms
        self.available_rooms = total_rooms

    def to_dict(self) -> Dict:
        """Convert object to dictionary."""
        return self.__dict__


class Customer:
    """Represents a customer."""

    def __init__(self, customer_id: int, name: str,
                 email: str, phone: str) -> None:
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone

    def to_dict(self) -> Dict:
        """Convert object to dictionary."""
        return self.__dict__


class Reservation:
    """Represents a reservation."""

    def __init__(self, reservation_id: int,
                 customer_id: int, hotel_id: int) -> None:
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id
        self.date = str(datetime.now())

    def to_dict(self) -> Dict:
        """Convert object to dictionary."""
        return self.__dict__


class HotelSystem:
    """Manages hotels, customers and reservations."""

    def __init__(self) -> None:
        self.hotels_file = "hotels.json"
        self.customers_file = "customers.json"
        self.reservations_file = "reservations.json"

    # -------------------------
    # HOTEL METHODS
    # -------------------------

    def create_hotel(self, hotel_id: int, name: str,
                     location: str, total_rooms: int) -> bool:
        hotels = load_data(self.hotels_file)

        if any(h["hotel_id"] == hotel_id for h in hotels):
            print("Hotel ID already exists.")
            return False

        hotel = Hotel(hotel_id, name, location, total_rooms)
        hotels.append(hotel.to_dict())
        save_data(self.hotels_file, hotels)
        return True

    def delete_hotel(self, hotel_id: int) -> bool:
        hotels = load_data(self.hotels_file)
        new_hotels = [h for h in hotels if h["hotel_id"] != hotel_id]

        if len(new_hotels) == len(hotels):
            print("Hotel not found.")
            return False

        save_data(self.hotels_file, new_hotels)
        return True

    def display_hotels(self) -> List[Dict]:
        return load_data(self.hotels_file)

    def modify_hotel(self, hotel_id: int, **kwargs) -> bool:
        hotels = load_data(self.hotels_file)

        for hotel in hotels:
            if hotel["hotel_id"] == hotel_id:
                for key, value in kwargs.items():
                    if key in hotel:
                        hotel[key] = value
                save_data(self.hotels_file, hotels)
                return True

        print("Hotel not found.")
        return False

    # -------------------------
    # CUSTOMER METHODS
    # -------------------------

    def create_customer(self, customer_id: int, name: str,
                        email: str, phone: str) -> bool:
        customers = load_data(self.customers_file)

        if any(c["customer_id"] == customer_id for c in customers):
            print("Customer ID already exists.")
            return False

        customer = Customer(customer_id, name, email, phone)
        customers.append(customer.to_dict())
        save_data(self.customers_file, customers)
        return True

    def delete_customer(self, customer_id: int) -> bool:
        customers = load_data(self.customers_file)
        new_customers = [
            c for c in customers if c["customer_id"] != customer_id
        ]

        if len(new_customers) == len(customers):
            print("Customer not found.")
            return False

        save_data(self.customers_file, new_customers)
        return True

    def display_customers(self) -> List[Dict]:
        return load_data(self.customers_file)

    def modify_customer(self, customer_id: int, **kwargs) -> bool:
        customers = load_data(self.customers_file)

        for customer in customers:
            if customer["customer_id"] == customer_id:
                for key, value in kwargs.items():
                    if key in customer:
                        customer[key] = value
                save_data(self.customers_file, customers)
                return True

        print("Customer not found.")
        return False

    # -------------------------
    # RESERVATION METHODS
    # -------------------------

    def create_reservation(self, reservation_id: int,
                           customer_id: int,
                           hotel_id: int) -> bool:
        reservations = load_data(self.reservations_file)
        hotels = load_data(self.hotels_file)
        customers = load_data(self.customers_file)

        if any(r["reservation_id"] == reservation_id
               for r in reservations):
            print("Reservation ID already exists.")
            return False

        if not any(c["customer_id"] == customer_id
                   for c in customers):
            print("Customer does not exist.")
            return False

        for hotel in hotels:
            if hotel["hotel_id"] == hotel_id:
                if hotel["available_rooms"] <= 0:
                    print("No available rooms.")
                    return False
                hotel["available_rooms"] -= 1
                reservation = Reservation(
                    reservation_id, customer_id, hotel_id
                )
                reservations.append(reservation.to_dict())
                save_data(self.hotels_file, hotels)
                save_data(self.reservations_file, reservations)
                return True

        print("Hotel does not exist.")
        return False

    def cancel_reservation(self, reservation_id: int) -> bool:
        reservations = load_data(self.reservations_file)
        hotels = load_data(self.hotels_file)

        for reservation in reservations:
            if reservation["reservation_id"] == reservation_id:
                for hotel in hotels:
                    if hotel["hotel_id"] == reservation["hotel_id"]:
                        hotel["available_rooms"] += 1
                reservations.remove(reservation)
                save_data(self.hotels_file, hotels)
                save_data(self.reservations_file, reservations)
                return True

        print("Reservation not found.")
        return False

    def display_reservations(self) -> List[Dict]:
        return load_data(self.reservations_file)