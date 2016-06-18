# -*- coding:utf-8 -*-
import unittest

from mylib.primes import is_prime, print_next_prime


#from unittest.mylib import MagicMock, Mock
#from mylib.rm_module import ProductionClass


class PrimesTestCase(unittest.TestCase):
    """Tests for `primes.py`.
        默认以test为开头的方法
    """

    def test_is_five_prime(self):
        """Is five successfully determined to be prime?"""
        self.assertTrue(is_prime(5))
        self.assertTrue(is_prime(7))

    def test_is_eight_not_prime(self):
        """Is eight successfully determined to be prime?"""
        self.assertFalse(is_prime(8), msg="eight is not prime")

    def test_is_zero_not_prime(self):
        """Is zero correctly determined not to be prime?"""
        self.assertFalse(is_prime(0))

    def test_negative_number(self):
        """Is a negative number correctly determined not to be prime?"""
        for index in range(-1, -10, -1):
            self.assertFalse(is_prime(index), msg='{} should not be determined to be prime'.format(index))

    def test_next_prime(self):
        print_next_prime(5)

if __name__ == '__main__':
    unittest.main()
