#!/usr/bin/python3
"""Defines a Review class"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Defines a Review class"""
    place_id = ""
    user_id = ""
    text = ""
