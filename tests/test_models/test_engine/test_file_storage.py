#!/usr/bin/python3
"""Unittests for Storage class"""

import unittest
import json
import os
import models
from datetime import datetime
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestFileStorage(unittest.TestCase):
    """Unittests for FileStorage class"""
    def test_init(self):
        self.assertEqual(type(FileStorage()), FileStorage)
        self.assertEqual(type(models.storage), FileStorage)
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_private_attributes(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))


class TestFileStorage_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("temp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        b1 = BaseModel()
        models.storage.new(b1)
        self.assertIn("BaseModel." + b1.id, models.storage.all().keys())
        self.assertIn(b1, models.storage.all().values())
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save(self):
        b1 = BaseModel()
        models.storage.new(b1)

    def test_reload(self):
        b1 = BaseModel()
        models.storage.new(b1)
        models.storage.save()
        models.storage.reload()
        objests = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + b1.id, objests)

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
