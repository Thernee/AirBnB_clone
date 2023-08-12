#!/usr/bin/python3
"""Unittests for class State"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlace(unittest.TestCase):
    """Tests class Place and its methods"""

    def test_init(self):
        """Tests instantions of a new instance"""
        place = Place()
        self.assertEqual(Place, type(Place()))
        self.assertEqual(str, type(Place().id))
        self.assertEqual(datetime, type(Place().created_at))
        self.assertEqual(datetime, type(Place().updated_at))
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(place))
        self.assertNotIn("city_id", place.__dict__)
        self.assertIn(Place(), models.storage.all().values())

    def test_public_attributes(self):
        place = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(place))
        self.assertNotIn("user_id", place.__dict__)
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(place))
        self.assertNotIn("name", place.__dict__)
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(place))
        self.assertNotIn("desctiption", place.__dict__)
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(place))
        self.assertNotIn("number_rooms", place.__dict__)
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(place))
        self.assertNotIn("number_bathrooms", place.__dict__)
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(place))
        self.assertNotIn("max_guest", place.__dict__)
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(place))
        self.assertNotIn("price_by_night", place.__dict__)
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(place))
        self.assertNotIn("latitude", place.__dict__)
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(place))
        self.assertNotIn("longitude", place.__dict__)
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(place))
        self.assertNotIn("amenity_ids", place.__dict__)

    def test_unique_id(self):
        """Tests that each instant has a unique id"""
        place1 = Place()
        place2 = Place()
        self.assertNotEqual(place1.id, place2.id)

    def test_datetime(self):
        """Tests created_at and updated_at
        public attributes"""
        place1 = Place()
        sleep(0.05)
        place2 = Place()
        self.assertLess(place1.created_at, place2.created_at)
        place3 = Place()
        sleep(0.05)
        place4 = Place()
        self.assertLess(place3.updated_at, place4.updated_at)

    def test_str_(self):
        """Tests str representation of instant"""
        date = datetime.today()
        date_repr = repr(date)
        place = Place()
        place.id = "123456"
        place.created_at = place.updated_at = date
        placestr = place.__str__()
        self.assertIn("[Place] (123456)", placestr)
        self.assertIn("'id': '123456'", placestr)
        self.assertIn("'created_at': " + date_repr, placestr)
        self.assertIn("'updated_at': " + date_repr, placestr)

    def test_args_unused(self):
        """Tests args"""
        place = Place(None)
        self.assertNotIn(None, place.__dict__.values())

    def test_with_kwargs(self):
        """Tests with kwargs"""
        date = datetime.today()
        date_iso = date.isoformat()
        place = Place(id="345", created_at=date_iso, updated_at=date_iso)
        self.assertEqual(place.id, "345")
        self.assertEqual(place.created_at, date)
        self.assertEqual(place.updated_at, date)

    def test_instantiation_with_None_kwargs(self):
        """Tests with no kwargs"""
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_save(self):
        """Tests saving"""
        place = Place()
        sleep(0.05)
        first_update = place.updated_at
        place.save()
        self.assertLess(first_update, place.updated_at)

    def test_two_saves(self):
        """Tests saving twice"""
        place = Place()
        sleep(0.05)
        first_update = place.updated_at
        place.save()
        second_update = place.updated_at
        self.assertLess(first_update, second_update)
        sleep(0.05)
        place.save()
        self.assertLess(second_update, place.updated_at)

    def test_save_with_arg(self):
        """Test saving with args"""
        place = Place()
        with self.assertRaises(TypeError):
            place.save(None)

    def test_save_updates_file(self):
        """Tests saving to file"""
        place = Place()
        place.save()
        placeid = "Place." + place.id
        with open("file.json", "r") as file:
            self.assertIn(placeid, file.read())

    def test_to_dict(self):
        """Tests to_dict method"""
        self.assertTrue(dict, type(Place().to_dict()))
        place = Place()
        place.name = "Arizona"
        self.assertIn("id", place.to_dict())
        self.assertIn("created_at", place.to_dict())
        self.assertIn("updated_at", place.to_dict())
        self.assertIn("__class__", place.to_dict())
        self.assertEqual("Arizona", place.name)

    def test_to_dict_type(self):
        """Tests to dict data type"""
        place = Place()
        place_dict = place.to_dict()
        self.assertEqual(str, type(place_dict["id"]))
        self.assertEqual(str, type(place_dict["created_at"]))
        self.assertEqual(str, type(place_dict["updated_at"]))

    def test_to_dict_output(self):
        """Tests output"""
        date = datetime.today()
        place_dict = Place()
        place_dict.id = "123456"
        place_dict.created_at = place_dict.updated_at = date
        tdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': date.isoformat(),
            'updated_at': date.isoformat(),
        }
        self.assertDictEqual(place_dict.to_dict(), tdict)
        self.assertNotEqual(place_dict.to_dict(), place_dict.__dict__)
        with self.assertRaises(TypeError):
            place_dict.to_dict(None)


if __name__ == "__main__":
    unittest.main()
