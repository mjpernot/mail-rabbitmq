#!/usr/bin/python
# Classification (U)

"""Program:  parse_email.py

    Description:  Unit testing of parse_email in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/parse_email.py

    Arguments:
        None

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
import mock

# Local
sys.path.append(os.getcwd())
import mail_2_rmq
import version

# Version
__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Super-Class:  unittest.TestCase

    Sub-Classes:  None

    Methods:
        setUp -> Unit testing initilization.
        test_parse_email -> Test parsing an email.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:
            None

        """

        self.raw_msg = "Raw Email Message"

    @mock.patch("mail_2_rmq.email.message_from_string")
    @mock.patch("mail_2_rmq.sys.stdin")
    def test_parse_email(self, mock_stdin, mock_parse):

        """Function:  test_parse_email

        Description:  Test parsing an email.

        Arguments:
            mock_stdin -> Mock Ref:  mail_2_rmq.sys.stdin
            mock_parse -> Mock Ref:  mail_2_rmq.email.message_from_string

        """

        mock_stdin.readlines.return_value = self.raw_msg
        mock_parse.return_value = "Raw Email Message"

        self.assertEqual(mail_2_rmq.parse_email(), self.raw_msg)


if __name__ == "__main__":
    unittest.main()
