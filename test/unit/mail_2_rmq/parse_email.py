# Classification (U)

"""Program:  parse_email.py

    Description:  Unit testing of parse_email in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/parse_email.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import mail_2_rmq                               # pylint:disable=E0401,C0413
import version                                  # pylint:disable=C0413,E0401

__version__ = version.__version__


class ParserTest():                                     # pylint:disable=R0903

    """Class:  ParserTest

    Description:  Class which is a representation of the email.Parser
        class.

    Methods:
        __init__
        parsestr

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the RQTest class.

        Arguments:

        """

    def parsestr(self, msg):

        """Method:  parsestr

        Description:  Stub holder for parsestr method.

        Arguments:

        """

        return msg


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_parse_email

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.raw_msg = ["Raw", "Email", "Message"]
        self.part = ParserTest()
        self.processed_msg = "RawEmailMessage"

    @mock.patch("mail_2_rmq.Parser")
    @mock.patch("mail_2_rmq.sys.stdin")
    def test_parse_email(self, mock_stdin, mock_parse):

        """Function:  test_parse_email

        Description:  Test parsing an email.

        Arguments:

        """

        mock_parse.return_value = self.part
        mock_stdin.readlines.return_value = self.raw_msg

        self.assertEqual(mail_2_rmq.parse_email(), self.processed_msg)


if __name__ == "__main__":
    unittest.main()
