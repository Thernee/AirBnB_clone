#!/usr/bin/python3
"""Unittests for class State"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    """Tests class Amenity and its methods"""

    def test_init(self):
        """Tests instantions of a new instance"""
        amenity = Amenity()
        self.assertEqual(Amenity, type(Amenity()))
        self.assertEqual(str, type(Amenity().id))
        self.assertEqual(datetime, type(Amenity().created_at))
        self.assertEqual(datetime, type(Amenity().updated_at))
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", amenity.__dict__)
        self.assertIn(Amenity(), models.storage.all().values())

    def test_unique_id(self):
        """Tests that each instant has a unique id"""
        amentiy1 = Amenity()
        amentiy2 = Amenity()
        self.assertNotEqual(amentiy1.id, amentiy2.id)

    def test_datetime(self):
        """Tests created_at and updated_at
        public attributes"""
        amentiy1 = Amenity()
        sleep(0.05)
        amentiy2 = Amenity()
        self.assertLess(amentiy1.created_at, amentiy2.created_at)
        amentiy3 = Amenity()
        sleep(0.05)
        amentiy4 = Amenity()
        self.assertLess(amentiy3.updated_at, amentiy4.updated_at)

    def test_str_(self):
        """Tests str representation of instant"""
        date = datetime.today()
        date_repr = repr(date)
        amenity = Amenity()
        amenity.id = "123456"
        amenity.created_at = amenity.updated_at = date
        amenitystr = amenity.__str__()
        self.assertIn("[Amenity] (123456)", amenitystr)
        self.assertIn("'id': '123456'", amenitystr)
        self.assertIn("'created_at': " + date_repr, amenitystr)
        self.assertIn("'updated_at': " + date_repr, amenitystr)

    def test_args_unused(self):
        """Tests args"""
        amentiy = Amenity(None)
        self.assertNotIn(None, amentiy.__dict__.values())

    def test_with_kwargs(self):
        """Tests with kwargs"""
        date = datetime.today()
        date_iso = date.isoformat()
        amentiy = Amenity(id="123", created_at=date_iso, updated_at=date_iso)
        self.assertEqual(amentiy.id, "123")
        self.assertEqual(amentiy.created_at, date)
        self.assertEqual(amentiy.updated_at, date)

    def test_instantiation_with_None_kwargs(self):
        """Tests with no kwargs"""
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)

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
        amentiy = Amenity()
        sleep(0.05)
        first_update = amentiy.updated_at
        amentiy.save()
        self.assertLess(first_update, amentiy.updated_at)

    def test_two_saves(self):
        """Tests saving twice"""
        amentiy = Amenity()
        sleep(0.05)
        first_update = amentiy.updated_at
        amentiy.save()
        second_update = amentiy.updated_at
        self.assertLess(first_update, second_update)
        sleep(0.05)
        amentiy.save()
        self.assertLess(second_update, amentiy.updated_at)

    def test_save_with_arg(self):
        """Test saving with args"""
        amentiy = Amenity()
        with self.assertRaises(TypeError):
            amentiy.save(None)

    def test_save_updates_file(self):
        """Tests saving to file"""
        amenity = Amenity()
        amenity.save()
        amenityid = "Amenity." + amenity.id
        with open("file.json", "r") as file:
            self.assertIn(amenityid, file.read())

    def test_to_dict(self):
        """Tests to_dict method"""
        self.assertTrue(dict, type(Amenity().to_dict()))
        amentiy = Amenity()
        amentiy.name = "Arizona"
        self.assertIn("name", amentiy.to_dict())
        self.assertIn("created_at", amentiy.to_dict())
        self.assertIn("updated_at", amentiy.to_dict())
        self.assertIn("__class__", amentiy.to_dict())
        self.assertEqual("Arizona", amentiy.name)

    def test_to_dict_type(self):
        """Tests to dict data type"""
        amentiy = Amenity()
        amentiy_dict = amentiy.to_dict()
        self.assertEqual(str, type(amentiy_dict["id"]))
        self.assertEqual(str, type(amentiy_dict["created_at"]))
        self.assertEqual(str, type(amentiy_dict["updated_at"]))

    def test_to_dict_output(self):
        """Tests output"""
        date = datetime.today()
        amentiy_dict = Amenity()
        amentiy_dict.id = "123456"
        amentiy_dict.created_at = amentiy_dict.updated_at = date
        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': date.isoformat(),
            'updated_at': date.isoformat(),
        }
        self.assertDictEqual(amentiy_dict.to_dict(), tdict)
        self.assertNotEqual(amentiy_dict.to_dict(), amentiy_dict.__dict__)
        with self.assertRaises(TypeError):
            amentiy_dict.to_dict(None)


if __name__ == "__main__":
    unittest.main()
