#!/usr/bin/python
# Classification (U)

"""Program:  check_nonprocess.py

    Description:  Unit testing of check_nonprocess in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/check_nonprocess.py

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
        test_check_nonprocess

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        pass

    def test_check_nonprocess(self):

        """Function:  test_check_nonprocess

        Description:  Test processing of non-processed emails.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mail_2_rmq.check_nonprocess("", ""))


if __name__ == "__main__":
    unittest.main()
