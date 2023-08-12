#!/usr/bin/python3
"""Unittests for the BaseModel Class"""

import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):

    def test_init(self):
        """Tests instantions of a new instance"""
        b1 = BaseModel()
        self.assertEqual(BaseModel, type(b1))
        self.assertEqual(str(type(b1)),
                         "<class 'models.base_model.BaseModel'>")
        self.assertIsInstance(b1, BaseModel)
        self.assertTrue(issubclass(type(b1), BaseModel))

    def test_unique_id(self):
        """Tests that each instant has a unique id"""
        b1 = BaseModel()
        b2 = BaseModel()
        self.assertEqual(str, type(b1.id))
        self.assertNotEqual(b1.id, b2.id)
        arr = [BaseModel().id for i in range(5)]
        self.assertEqual(len(set(arr)), len(arr))

    def test_datetime(self):
        """Tests created_at and updated_at
        public attributes"""
        b1 = BaseModel()
        self.assertEqual(datetime, type(b1.created_at))
        self.assertEqual(datetime, type(b1.updated_at))

    def test_two_models_different_created_at(self):
        b1 = BaseModel()
        sleep(0.05)
        b2 = BaseModel()
        self.assertLess(b1.created_at, b2.created_at)

    def test_two_models_different_updated_at(self):
        b1 = BaseModel()
        sleep(0.05)
        b2 = BaseModel()
        self.assertLess(b1.updated_at, b2.updated_at)

    def test_to_dict(self):
        """Tests the to_dict public method"""
        b1 = BaseModel()
        b1.name = "Jack"
        b1.age = 20
        d = b1.to_dict()
        self.assertEqual(dict, type(d))
        self.assertNotEqual(d, b1.__dict__)
        self.assertIn("created_at", d)
        self.assertIn("updated_at", d)
        self.assertIn("name", d)
        self.assertIn("age", d)
        self.assertIn("__class__", d)
        self.assertEqual(d['id'], b1.id)
        self.assertEqual(d['created_at'], b1.created_at.isoformat())
        self.assertEqual(d['updated_at'], b1.updated_at.isoformat())
        self.assertEqual(d['__class__'], type(b1).__name__)
        self.assertEqual(d['name'], b1.name)
        self.assertEqual(d['age'], b1.age)
        self.assertEqual(str, type(d["created_at"]))
        self.assertEqual(str, type(d["updated_at"]))

    def test_to_dict_output(self):
        """Test output"""
        date = datetime.today()
        b1 = BaseModel()
        b1.id = "456654"
        b1.created_at = b1.updated_at = date
        tdict = {
            'id': '456654',
            '__class__': 'BaseModel',
            'created_at': date.isoformat(),
            'updated_at': date.isoformat()
        }
        self.assertDictEqual(b1.to_dict(), tdict)

    def test_to_dict_with_arg(self):
        """Dictionary with args"""
        b1 = BaseModel()
        with self.assertRaises(TypeError):
            b1.to_dict(None)

    def test_save(self):
        """Test save functionality"""
        b1 = BaseModel()
        sleep(0.05)
        first_update = b1.updated_at
        b1.save()
        self.assertLess(first_update, b1.updated_at)

    def test_save_twice(self):
        """Test save twice"""
        b1 = BaseModel()
        sleep(0.05)
        first_update = b1.updated_at
        b1.save()
        second_update = b1.updated_at
        self.assertLess(first_update, second_update)
        sleep(0.05)
        b1.save()
        self.assertLess(second_update, b1.updated_at)

    def test_save_with_arg(self):
        """Tests save with arguments"""
        b1 = BaseModel()
        with self.assertRaises(TypeError):
            b1.save(None)

    def test_save_updates_file(self):
        """Tests save to file"""
        b1 = BaseModel()
        b1.save()
        b1id = "BaseModel." + b1.id
        with open("file.json", "r") as f:
            self.assertIn(b1id, f.read())

    def test_str_(self):
        """Tests str representation of instant"""
        date = datetime.today()
        date_repr = repr(date)
        b1 = BaseModel()
        b1.id = "456654"
        b1.created_at = b1.updated_at = date
        b1str = b1.__str__()
        self.assertIn("[BaseModel] (456654)", b1str)
        self.assertIn("'id': '456654'", b1str)
        self.assertIn("'created_at': " + date_repr, b1str)
        self.assertIn("'updated_at': " + date_repr, b1str)

    def test_args_unused(self):
        """Tests with no args"""
        b1 = BaseModel(None)
        self.assertNotIn(None, b1.__dict__.values())

    def test_with_kwargs(self):
        """Tests with kwargs"""
        date = datetime.today()
        date_iso = date.isoformat()
        b1 = BaseModel(id="123", created_at=date_iso, updated_at=date_iso)
        self.assertEqual(b1.id, "123")
        self.assertEqual(b1.created_at, date)
        self.assertEqual(b1.updated_at, date)

    def test_with_no_kwargs(self):
        """Tests with no kwargs"""
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_with_args_and_kwargs(self):
        """Tests with args and kwargs"""
        date = datetime.today()
        date_iso = date.isoformat()
        b1 = BaseModel("12", id="345",
                       created_at=date_iso, updated_at=date_iso)
        self.assertEqual(b1.id, "345")
        self.assertEqual(b1.created_at, date)
        self.assertEqual(b1.updated_at, date)


if __name__ == '__main__':
    unittest.main()
