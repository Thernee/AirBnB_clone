#!/usr/bin/python3

import unittest
import uuid
import models.base_model as base_module
from models.base_model import BaseModel
from datetime import datetime

""" Define a test class for Basemodel class."""


class TestBaseModel(unittest.TestCase):
    """Declare TestBaseMode class for testing BaseModel class."""

    def setUp(self):
        """ Assign values for tests."""

    def tearDown(self):
        """clean up after each test."""

    def test_module_doc(self):
        """ test module documentation."""
        self.assertTrue(base_module.__doc__ is not None)

    def test_BaseModel_doc(self):
        """ test BaseModel class documentation."""
        self.assertTrue(BaseModel.__doc__ is not None)

    def test_id_uniqueness(self):
        """Test how unique created ids are."""
        test_objects = [BaseModel() for _ in range(10)]

        for i in range(len(test_objects)):
            for j in range(i + 1, len(test_objects)):
                self.assertNotEqual(test_objects[i].id, test_objects[j].id)

    def check_uuid(id):
        """check if id is valid uuid."""
        try:
            uuid.UUID(str(id))
            return True
        except ValueError:
            return False

    def test_id_validity(self):
        """check if id is a valid uuid."""
        test_objs = [BaseModel() for _ in range(10)]

        for i in range(len(test_objs)):
            id = test_objs[i].id
            self.assertTrue(check_uuid(id))

    def test_created_at(self):
        """ check if created_at is set at current datetime."""
        test = BaseModel()
        self.assertAlmostEqual(test.created_at, datetime.today(),
                               delta=datetime.timedelta(seconds=5))

    def test_updated_at(self):
        """ check if updated_at is set at current datetime."""
        test1 = BaseModel()
        self.assertAlmostEqual(test.created_at, datetime.today(),
                               delta=datetime.timedelta(seconds=5))

    def test_instance_update(self):
        """check if updated_at is update with each instance update."""
        test = BaseModel()
        initial = test.updated_at
        test.save()
        updated = test.updated_at

        self.assertNotEqual(initial, updated)
