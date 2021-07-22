#!/usr/bin/python
# Classification (U)

"""Program:  help_message.py

    Description:  Unit testing of help_message in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/help_message.py

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
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_help_message

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        pass

    def test_help_message(self):

        """Function:  test_help_message

        Description:  Test help message.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mail_2_rmq.help_message())


if __name__ == "__main__":
    unittest.main()
