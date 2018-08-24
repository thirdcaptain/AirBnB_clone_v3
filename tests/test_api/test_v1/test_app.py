#!/usr/bin/python3
"""
tests the app module
"""

import unittest
import flask
from api.v1.app import app


class AppTest(unittest.TestCase):
    """
    test the app module
    """

    def test_create_app(self):
        """
        check app creation
        """
        with app.test_client() as c:
            self.assertIsInstance(c, flask.testing.FlaskClient)
