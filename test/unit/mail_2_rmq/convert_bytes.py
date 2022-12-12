# Classification (U)

"""Program:  convert_bytes.py

    Description:  Unit testing of convert_bytes in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/convert_bytes.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest

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
        test_conversion

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.data = "Data String"
        self.results2 = "Data String"
        self.results3 = b"Data String"

    def test_conversion(self):

        """Function:  test_conversion

        Description:  Test conversion based on Python version.

        Arguments:

        """

        results = self.results2 if sys.version_info < (3, 0) else self.results3

        self.assertEqual(mail_2_rmq.convert_bytes(self.data), results)


if __name__ == "__main__":
    unittest.main()
