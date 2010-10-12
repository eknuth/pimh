"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from diy.models import DIY_Neighborhood

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

class DIY_Neighborhoods(TestCase):
    def test_create_poly(self):
        """
        Create Neighborhood
        """
        name = 'name'
        n = DIY_Neighborhood.create_from_string('name', 
                              'POINT(-122.65205993652 45.53),POINT(-122.65205993652 45.525193481445),POINT(-122.63008728027 45.525880126953),POINT(-122.62940063477 45.55815246582)')
        self.failUnlessEqual(name, n.name)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

