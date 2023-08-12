#!/usr/bin/python3
"""Unittests for class City"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCity(unittest.TestCase):
    """Tests class City and its methods"""

    def test_init(self):
        """Tests instantions of a new instance"""
        city = City()
        self.assertEqual(City, type(City()))
        self.assertEqual(str, type(City().id))
        self.assertEqual(datetime, type(City().created_at))
        self.assertEqual(datetime, type(City().updated_at))
        self.assertEqual(str, type(City.state_id))
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(city))
        self.assertNotIn("name", city.__dict__)
        self.assertIn(City(), models.storage.all().values())
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(city))
        self.assertNotIn("state_id", city.__dict__)

    def test_unique_id(self):
        """Tests that each instant has a unique id"""
        city1 = City()
        city2 = City()
        self.assertNotEqual(city1.id, city2.id)

    def test_datetime(self):
        """Tests created_at and updated_at
        public attributes"""
        city1 = City()
        sleep(0.05)
        city2 = City()
        self.assertLess(city1.created_at, city2.created_at)
        city3 = City()
        sleep(0.05)
        city4 = City()
        self.assertLess(city3.updated_at, city4.updated_at)

    def test_str_(self):
        """Tests str representation of instant"""
        date = datetime.today()
        date_rep = repr(date)
        city = City()
        city.id = "123456"
        city.created_at = city.updated_at = date
        citystr = city.__str__()
        self.assertIn("[City] (123456)", citystr)
        self.assertIn("'id': '123456'", citystr)
        self.assertIn("'created_at': " + date_rep, citystr)
        self.assertIn("'updated_at': " + date_rep, citystr)

    def test_args_unused(self):
        """Tests args"""
        city = City(None)
        self.assertNotIn(None, city.__dict__.values())

    def test_with_kwargs(self):
        """Tests with kwargs"""
        date = datetime.today()
        date_iso = date.isoformat()
        city = City(id="123", created_at=date_iso, updated_at=date_iso)
        self.assertEqual(city.id, "123")
        self.assertEqual(city.created_at, date)
        self.assertEqual(city.updated_at, date)

    def test_instantiation_with_None_kwargs(self):
        """Tests with no kwargs"""
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)

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
        city = City()
        sleep(0.05)
        first_update = city.updated_at
        city.save()
        self.assertLess(first_update, city.updated_at)

    def test_two_saves(self):
        """Tests saving twice"""
        city = City()
        sleep(0.05)
        first_update = city.updated_at
        city.save()
        second_update = city.updated_at
        self.assertLess(first_update, second_update)
        sleep(0.05)
        city.save()
        self.assertLess(second_update, city.updated_at)

    def test_save_with_arg(self):
        """Test saving with args"""
        city = City()
        with self.assertRaises(TypeError):
            city.save(None)

    def test_save_updates_file(self):
        """Tests saving to file"""
        city = City()
        city.save()
        usid = "City." + city.id
        with open("file.json", "r") as f:
            self.assertIn(usid, f.read())

    def test_to_dict(self):
        """Tests to_dict method"""
        self.assertTrue(dict, type(City().to_dict()))
        city = City()
        city.name = "Paris"
        city.state_id = "123321"
        self.assertIn("id", city.to_dict())
        self.assertIn("created_at", city.to_dict())
        self.assertIn("updated_at", city.to_dict())
        self.assertIn("__class__", city.to_dict())
        self.assertEqual("Paris", city.name)
        self.assertEqual("123321", city.state_id)

    def test_to_dict_type(self):
        """Tests to dict data type"""
        city = City()
        city_dict = city.to_dict()
        self.assertEqual(str, type(city_dict["id"]))
        self.assertEqual(str, type(city_dict["created_at"]))
        self.assertEqual(str, type(city_dict["updated_at"]))

    def test_to_dict_output(self):
        """Tests output"""
        date = datetime.today()
        city = City()
        city.id = "123456"
        city.created_at = city.updated_at = date
        tdict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': date.isoformat(),
            'updated_at': date.isoformat(),
        }
        self.assertDictEqual(city.to_dict(), tdict)
        self.assertNotEqual(city.to_dict(), city.__dict__)
        with self.assertRaises(TypeError):
            city.to_dict(None)


if __name__ == "__main__":
    unittest.main()
