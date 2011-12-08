"""
tests.py -- Test suite for the Shorty App
"""

from django.test import TestCase
from basex import BaseX, BaseXError


class BaseXTest(TestCase):
    """Test suite for BaseX.py library"""

    def test_basex_encoding(self):
        """Test basex with an integer"""
        s = BaseX(number=100)
        self.assertEqual('1C', s.encoded)
        self.assertEqual(100, s.number)

    def test_basex_decoding(self):
        """Test basex with encoded string"""
        s = BaseX(encoded='2Jv')
        self.assertEqual(10509, s.number)
        self.assertEqual('2Jv', s.encoded)

    def test_basex_alternate_encoding(self):
        """Test basex encoding with alternate character set"""
        s = BaseX(number=99999, character_set="5AGZab")
        self.assertEqual('G5b5baZ', s.encoded)
        self.assertEqual(99999, s.number)

    def test_basex_alternate_decoding(self):
        """Test basex decoding with alternate character set"""
        s = BaseX(encoded='G5b5baZ', character_set="5AGZab")
        self.assertEqual(99999, s.number)
        self.assertEqual('G5b5baZ', s.encoded)
        self.assertEqual('5AGZab', s.character_set)

    def test_basex_outputs(self):
        """Test basex default outputs"""
        s = BaseX(number=100)
        self.assertEqual('1C', s.__str__())
        self.assertEqual(u'1C', s.__unicode__())
        self.assertEqual(100, s.__int__())

    def test_basex_character_set_error(self):
        """Test exception raised for dupe characters in character_set"""
        self.assertRaises(BaseXError,
                          BaseX,
                          number=100,
                          character_set="ABCD1234A98")

    def test_basex_no_input(self):
        """Test exception raised if no value supplied for number or encoded"""
        self.assertRaises(BaseXError, BaseX)
