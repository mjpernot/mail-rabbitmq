#!/usr/bin/python
# Classification (U)

"""Program:  main.py

    Description:  Unit testing of main in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/main.py

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
        test_help_true -> Test with Help_Func returns True.
        test_help_false -> Test with Help_Func returns False.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:
            None

        """

        self.args = {"-c": "config_file", "-d": "config_dir", "-M": True}
        self.func_dict = {"-M": mail_2_rmq.process_message,
                          "-C": mail_2_rmq.check_nonprocess}

    @mock.patch("mail_2_rmq.gen_libs.help_func")
    @mock.patch("mail_2_rmq.arg_parser.arg_parse2")
    def test_help_true(self, mock_arg, mock_help):

        """Function:  test_status_true

        Description:  Test main function with Help_Func returns True.

        Arguments:
            mock_arg -> Mock Ref:  mail_2_rmq.arg_parser.arg_parse2
            mock_help -> Mock Ref:  mail_2_rmq.gen_libs.help_func

        """

        mock_arg.return_value = self.args
        mock_help.return_value = True

        self.assertFalse(mail_2_rmq.main())


if __name__ == "__main__":
    unittest.main()
