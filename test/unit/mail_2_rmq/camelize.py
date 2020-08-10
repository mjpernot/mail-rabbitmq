#!/usr/bin/python
# Classification (U)

"""Program:  camelize.py

    Description:  Unit testing of camelize in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/camelize.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

# Third-party

# Local
sys.path.append(os.getcwd())
import mail_2_rmq
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Unit testing initilization.
        test_special_string -> Test with a string with special characters.
        test_numeric_string -> Test with a string with numerics in it.
        test_normal_string -> Test with a string with only characters.
        test_empty_string -> Test with an empty string.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.data_str = ""
        self.data_str1 = "This is a test of camel case"
        self.data_str2 = "This is a test with numer1cal numb5r5 in it"
        self.data_str3 = "This string h@s special chars' and other things."
        self.data_test = ""
        self.data_test1 = "ThisIsATestOfCamelCase"
        self.data_test2 = "ThisIsATestWithNumer1calNumb5r5InIt"
        self.data_test3 = "ThisStringHSSpecialCharsAndOtherThings"

    def test_special_string(self):

        """Function:  test_special_string

        Description:  Test with a string with special characters.

        Arguments:

        """

        self.assertEqual(mail_2_rmq.camelize(self.data_str3), self.data_test3)

    def test_numeric_string(self):

        """Function:  test_numeric_string

        Description:  Test with a string with numerics in it.

        Arguments:

        """

        self.assertEqual(mail_2_rmq.camelize(self.data_str2), self.data_test2)

    def test_normal_string(self):

        """Function:  test_normal_string

        Description:  Test with a string with only characters.

        Arguments:

        """

        self.assertEqual(mail_2_rmq.camelize(self.data_str1), self.data_test1)

    def test_empty_string(self):

        """Function:  test_empty_string

        Description:  Test with an empty string.

        Arguments:

        """

        self.assertEqual(mail_2_rmq.camelize(self.data_str), self.data_test)


if __name__ == "__main__":
    unittest.main()
