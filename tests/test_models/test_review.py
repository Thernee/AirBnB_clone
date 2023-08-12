#!/usr/bin/python3
"""Unittests for class Review"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReview(unittest.TestCase):
    """Tests class Review and its methods"""

    def test_init(self):
        """Tests instantions of a new instance"""
        review = Review()
        self.assertEqual(Review, type(Review()))
        self.assertEqual(str, type(Review().id))
        self.assertEqual(datetime, type(Review().created_at))
        self.assertEqual(datetime, type(Review().updated_at))
        self.assertEqual(str, type(review.place_id))
        self.assertEqual(str, type(review.user_id))
        self.assertEqual(str, type(review.text))
        self.assertIn("text", dir(review))
        self.assertNotIn("text", review.__dict__)
        self.assertIn(Review(), models.storage.all().values())
        self.assertIn("user_id", dir(review))
        self.assertNotIn("user_id", review.__dict__)

    def test_unique_id(self):
        """Tests that each instant has a unique id"""
        review1 = Review()
        review2 = Review()
        self.assertNotEqual(review1.id, review2.id)

    def test_datetime(self):
        """Tests created_at and updated_at
        public attributes"""
        review1 = Review()
        sleep(0.05)
        review2 = Review()
        self.assertLess(review1.created_at, review2.created_at)
        review3 = Review()
        sleep(0.05)
        review4 = Review()
        self.assertLess(review3.updated_at, review4.updated_at)

    def test_str_(self):
        """Tests str representation of instant"""
        date = datetime.today()
        date_rep = repr(date)
        review = Review()
        review.id = "123456"
        review.created_at = review.updated_at = date
        reviewstr = review.__str__()
        self.assertIn("[Review] (123456)", reviewstr)
        self.assertIn("'id': '123456'", reviewstr)
        self.assertIn("'created_at': " + date_rep, reviewstr)
        self.assertIn("'updated_at': " + date_rep, reviewstr)

    def test_args_unused(self):
        """Tests args"""
        review = Review(None)
        self.assertNotIn(None, review.__dict__.values())

    def test_with_kwargs(self):
        """Tests with kwargs"""
        date = datetime.today()
        date_iso = date.isoformat()
        review = Review(id="123", created_at=date_iso, updated_at=date_iso)
        self.assertEqual(review.id, "123")
        self.assertEqual(review.created_at, date)
        self.assertEqual(review.updated_at, date)

    def test_instantiation_with_None_kwargs(self):
        """Tests with no kwargs"""
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)

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
        review = Review()
        sleep(0.05)
        first_update = review.updated_at
        review.save()
        self.assertLess(first_update, review.updated_at)

    def test_two_saves(self):
        """Tests saving twice"""
        review = Review()
        sleep(0.05)
        first_update = review.updated_at
        review.save()
        second_update = review.updated_at
        self.assertLess(first_update, second_update)
        sleep(0.05)
        review.save()
        self.assertLess(second_update, review.updated_at)

    def test_save_with_arg(self):
        """Test saving with args"""
        review = Review()
        with self.assertRaises(TypeError):
            review.save(None)

    def test_save_updates_file(self):
        """Tests saving to file"""
        review = Review()
        review.save()
        usid = "Review." + review.id
        with open("file.json", "r") as f:
            self.assertIn(usid, f.read())

    def test_to_dict(self):
        """Tests to_dict method"""
        self.assertTrue(dict, type(Review().to_dict()))
        review = Review()
        review.place_id = "123321"
        review.user_id = "456654"
        review.text = "texttest"
        self.assertIn("place_id", review.to_dict())
        self.assertIn("created_at", review.to_dict())
        self.assertIn("updated_at", review.to_dict())
        self.assertIn("__class__", review.to_dict())
        self.assertEqual("texttest", review.text)
        self.assertEqual("456654", review.user_id)
        self.assertEqual("123321", review.place_id)

    def test_to_dict_type(self):
        """Tests to dict data type"""
        review = Review()
        review_dict = review.to_dict()
        self.assertEqual(str, type(review_dict["id"]))
        self.assertEqual(str, type(review_dict["created_at"]))
        self.assertEqual(str, type(review_dict["updated_at"]))

    def test_to_dict_output(self):
        """Tests output"""
        date = datetime.today()
        review = Review()
        review.id = "123456"
        review.created_at = review.updated_at = date
        tdict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': date.isoformat(),
            'updated_at': date.isoformat(),
        }
        self.assertDictEqual(review.to_dict(), tdict)
        self.assertNotEqual(review.to_dict(), review.__dict__)
        with self.assertRaises(TypeError):
            review.to_dict(None)


if __name__ == "__main__":
    unittest.main()
