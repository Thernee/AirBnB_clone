#!/usr/bin/python3
"""Unittests for class User"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUser(unittest.TestCase):
    """Tests class User and its methods"""

    def test_init(self):
        """Tests instantions of a new instance"""
        self.assertEqual(User, type(User()))
        self.assertEqual(str, type(User().id))
        self.assertEqual(datetime, type(User().created_at))
        self.assertEqual(datetime, type(User().updated_at))
        self.assertEqual(str, type(User.email))
        self.assertEqual(str, type(User.password))
        self.assertEqual(str, type(User.first_name))
        self.assertEqual(str, type(User.last_name))
        self.assertIn(User(), models.storage.all().values())

    def test_unique_id(self):
        """Tests that each instant has a unique id"""
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.id, user2.id)

    def test_datetime(self):
        """Tests created_at and updated_at
        public attributes"""
        user1 = User()
        sleep(0.05)
        user2 = User()
        self.assertLess(user1.created_at, user2.created_at)
        user3 = User()
        sleep(0.05)
        user4 = User()
        self.assertLess(user3.updated_at, user4.updated_at)

    def test_str_(self):
        """Tests str representation of instant"""
        date = datetime.today()
        date_rep = repr(date)
        user = User()
        user.id = "123456"
        user.created_at = user.updated_at = date
        userstr = user.__str__()
        self.assertIn("[User] (123456)", userstr)
        self.assertIn("'id': '123456'", userstr)
        self.assertIn("'created_at': " + date_rep, userstr)
        self.assertIn("'updated_at': " + date_rep, userstr)

    def test_args_unused(self):
        """Tests args"""
        us = User(None)
        self.assertNotIn(None, us.__dict__.values())

    def test_with_kwargs(self):
        """Tests with kwargs"""
        date = datetime.today()
        date_iso = date.isoformat()
        user = User(id="123", created_at=date_iso, updated_at=date_iso)
        self.assertEqual(user.id, "123")
        self.assertEqual(user.created_at, date)
        self.assertEqual(user.updated_at, date)

    def test_instantiation_with_None_kwargs(self):
        """Tests with no kwargs"""
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)

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
        user = User()
        sleep(0.05)
        first_update = user.updated_at
        user.save()
        self.assertLess(first_update, user.updated_at)

    def test_two_saves(self):
        """Tests saving twice"""
        user = User()
        sleep(0.05)
        first_update = user.updated_at
        user.save()
        second_update = user.updated_at
        self.assertLess(first_update, second_update)
        sleep(0.05)
        user.save()
        self.assertLess(second_update, user.updated_at)

    def test_save_with_arg(self):
        """Test saving with args"""
        user = User()
        with self.assertRaises(TypeError):
            user.save(None)

    def test_save_updates_file(self):
        """Tests saving to file"""
        user = User()
        user.save()
        usid = "User." + user.id
        with open("file.json", "r") as f:
            self.assertIn(usid, f.read())

    def test_to_dict(self):
        """Tests to_dict method"""
        self.assertTrue(dict, type(User().to_dict()))
        user = User()
        user.first_name = "Jack"
        user.last_name = "Jackson"
        self.assertIn("id", user.to_dict())
        self.assertIn("created_at", user.to_dict())
        self.assertIn("updated_at", user.to_dict())
        self.assertIn("__class__", user.to_dict())
        self.assertEqual("Jack", user.first_name)
        self.assertEqual("Jackson", user.last_name)

    def test_to_dict_type(self):
        """Tests to dict data type"""
        user = User()
        user_dict = user.to_dict()
        self.assertEqual(str, type(user_dict["id"]))
        self.assertEqual(str, type(user_dict["created_at"]))
        self.assertEqual(str, type(user_dict["updated_at"]))

    def test_to_dict_output(self):
        """Tests output"""
        date = datetime.today()
        user = User()
        user.id = "123456"
        user.created_at = user.updated_at = date
        tdict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': date.isoformat(),
            'updated_at': date.isoformat(),
        }
        self.assertDictEqual(user.to_dict(), tdict)
        self.assertNotEqual(user.to_dict(), user.__dict__)
        with self.assertRaises(TypeError):
            user.to_dict(None)


if __name__ == "__main__":
    unittest.main()
