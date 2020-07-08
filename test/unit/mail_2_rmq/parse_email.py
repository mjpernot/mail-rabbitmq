#!/usr/bin/python
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

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Unit testing initilization.
        test_parse_email -> Test parsing an email.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        class ParserTest(object):

            """Class:  ParserTest

            Description:  Class which is a representation of the email.Parser
                class.

            Methods:
                __init__ -> Initialize configuration environment.
                parsestr -> Stub holder for parsestr method.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the RQTest class.

                Arguments:

                """

                pass

            def parsestr(self, msg):

                """Method:  parsestr

                Description:  Stub holder for parsestr method.

                Arguments:

                """

                return msg

        self.raw_msg = ["Raw", "Email", "Message"]
        self.part = ParserTest()
        self.processed_msg = "RawEmailMessage"

    @mock.patch("mail_2_rmq.email.Parser")
    @mock.patch("mail_2_rmq.sys.stdin")
    def test_parse_email(self, mock_stdin, mock_parse):

        """Function:  test_parse_email

        Description:  Test parsing an email.

        Arguments:

        """

        mock_parse.Parser.return_value = self.part
        mock_stdin.readlines.return_value = self.raw_msg

        self.assertEqual(mail_2_rmq.parse_email(), self.processed_msg)


if __name__ == "__main__":
    unittest.main()
