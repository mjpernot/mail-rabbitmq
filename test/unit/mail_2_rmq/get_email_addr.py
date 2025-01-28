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
import unittest

# Local
sys.path.append(os.getcwd())
import mail_2_rmq                               # pylint:disable=E0401,C0413
import version                                  # pylint:disable=C0413,E0401

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_two_email
        test_one_email

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.data = "Data string name@mail.mil and some more."
        self.data2 = "Data string name@mail.mil and name1@gmail.com more."
        self.results = ["name@mail.mil"]
        self.results2 = ["name@mail.mil", "name1@gmail.com"]

    def test_two_email(self):

        """Function:  test_two_email

        Description:  Test with two email addresses.

        Arguments:

        """

        self.assertEqual(mail_2_rmq.get_email_addr(self.data2), self.results2)

    def test_one_email(self):

        """Function:  test_one_email

        Description:  Test with one email address.

        Arguments:

        """

        self.assertEqual(mail_2_rmq.get_email_addr(self.data), self.results)


if __name__ == "__main__":
    unittest.main()
