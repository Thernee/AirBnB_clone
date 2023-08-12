#!/usr/bin/python3
"""Unittests for class State"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestState(unittest.TestCase):
    """Tests class State and its methods"""

    def test_init(self):
        """Tests instantions of a new instance"""
        state = State()
        self.assertEqual(State, type(State()))
        self.assertEqual(str, type(State().id))
        self.assertEqual(datetime, type(State().created_at))
        self.assertEqual(datetime, type(State().updated_at))
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(state))
        self.assertNotIn("name", state.__dict__)
        self.assertIn(State(), models.storage.all().values())

    def test_unique_id(self):
        """Tests that each instant has a unique id"""
        state1 = State()
        state2 = State()
        self.assertNotEqual(state1.id, state2.id)

    def test_datetime(self):
        """Tests created_at and updated_at
        public attributes"""
        state1 = State()
        sleep(0.05)
        state2 = State()
        self.assertLess(state1.created_at, state2.created_at)
        state3 = State()
        sleep(0.05)
        state4 = State()
        self.assertLess(state3.updated_at, state4.updated_at)

    def test_str_(self):
        """Tests str representation of instant"""
        date = datetime.today()
        date_rep = repr(date)
        state = State()
        state.id = "123456"
        state.created_at = state.updated_at = date
        statestr = state.__str__()
        self.assertIn("[State] (123456)", statestr)
        self.assertIn("'id': '123456'", statestr)
        self.assertIn("'created_at': " + date_rep, statestr)
        self.assertIn("'updated_at': " + date_rep, statestr)

    def test_args_unused(self):
        """Tests args"""
        state = State(None)
        self.assertNotIn(None, state.__dict__.values())

    def test_with_kwargs(self):
        """Tests with kwargs"""
        date = datetime.today()
        date_iso = date.isoformat()
        state = State(id="123", created_at=date_iso, updated_at=date_iso)
        self.assertEqual(state.id, "123")
        self.assertEqual(state.created_at, date)
        self.assertEqual(state.updated_at, date)

    def test_instantiation_with_None_kwargs(self):
        """Tests with no kwargs"""
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)

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
        state = State()
        sleep(0.05)
        first_update = state.updated_at
        state.save()
        self.assertLess(first_update, state.updated_at)

    def test_two_saves(self):
        """Tests saving twice"""
        state = State()
        sleep(0.05)
        first_update = state.updated_at
        state.save()
        second_update = state.updated_at
        self.assertLess(first_update, second_update)
        sleep(0.05)
        state.save()
        self.assertLess(second_update, state.updated_at)

    def test_save_with_arg(self):
        """Test saving with args"""
        state = State()
        with self.assertRaises(TypeError):
            state.save(None)

    def test_save_updates_file(self):
        """Tests saving to file"""
        state = State()
        state.save()
        usid = "State." + state.id
        with open("file.json", "r") as f:
            self.assertIn(usid, f.read())

    def test_to_dict(self):
        """Tests to_dict method"""
        self.assertTrue(dict, type(State().to_dict()))
        state = State()
        state.name = "Arizona"
        self.assertIn("name", state.to_dict())
        self.assertIn("created_at", state.to_dict())
        self.assertIn("updated_at", state.to_dict())
        self.assertIn("__class__", state.to_dict())
        self.assertEqual("Arizona", state.name)

    def test_to_dict_type(self):
        """Tests to dict data type"""
        state = State()
        state_dict = state.to_dict()
        self.assertEqual(str, type(state_dict["id"]))
        self.assertEqual(str, type(state_dict["created_at"]))
        self.assertEqual(str, type(state_dict["updated_at"]))

    def test_to_dict_output(self):
        """Tests output"""
        date = datetime.today()
        state_dict = State()
        state_dict.id = "123456"
        state_dict.created_at = state_dict.updated_at = date
        tdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': date.isoformat(),
            'updated_at': date.isoformat(),
        }
        self.assertDictEqual(state_dict.to_dict(), tdict)
        self.assertNotEqual(state_dict.to_dict(), state_dict.__dict__)
        with self.assertRaises(TypeError):
            state_dict.to_dict(None)


if __name__ == "__main__":
    unittest.main()
