#!/usr/bin/python
# Classification (U)

"""Program:  get_email_addr.py

    Description:  Unit testing of get_email_addr in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/get_email_addr.py

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
        setUp
        test_special_chars
        test_from_line
        test_multiple_find
        test_single_find
        test_no_find
        test_empty_string

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.data = ""
        self.data2 = "There is nothing in this string"
        self.data3 = "This a string with my.name@email.domain in string"
        self.data4 = "This has 2: my.name@email.domain & mine@nodomain.domain"
        self.data5 = "From Mine Name my.name@email.domain"
        self.data6 = "From Mine Name <my.name@email.domain>"
        self.result = list()
        self.result2 = ["my.name@email.domain"]
        self.result3 = ["my.name@email.domain", "mine@nodomain.domain"]

    def test_special_chars(self):

        """Function:  test_special_chars

        Description:  Test with < and > characters on either side of address.

        Arguments:

        """

        self.assertEqual(mail_2_rmq.get_email_addr(self.data6), self.result2)

    def test_from_line(self):

        """Function:  test_from_line

        Description:  Test with a string in the format of a From line.

        Arguments:

        """

        self.assertEqual(mail_2_rmq.get_email_addr(self.data5), self.result2)

    def test_multiple_find(self):

        """Function:  test_multiple_find

        Description:  Test with a string with multiple email addresses.

        Arguments:

        """

        self.assertEqual(mail_2_rmq.get_email_addr(self.data4), self.result3)

    def test_single_find(self):

        """Function:  test_single_find

        Description:  Test with a string with a single email address.

        Arguments:

        """

        self.assertEqual(mail_2_rmq.get_email_addr(self.data3), self.result2)

    def test_no_find(self):

        """Function:  test_no_find

        Description:  Test with a string with no email addresses.

        Arguments:

        """

        self.assertEqual(mail_2_rmq.get_email_addr(self.data2), self.result)

    def test_empty_string(self):

        """Function:  test_empty_string

        Description:  Test with an empty string.

        Arguments:

        """

        self.assertEqual(mail_2_rmq.get_email_addr(self.data), self.result)


if __name__ == "__main__":
    unittest.main()
