#!/usr/bin/python
# Classification (U)

"""Program:  main.py

    Description:  Unit testing of main in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/main.py

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
        setUp
        test_dir_chk_crt_false
        test_dir_chk_crt_true-> Test with arg_dir_chk_crt returns True.
        test_xor_dict_true
        test_xor_dict_false
        test_require_false
        test_require_true
        test_help_false
        test_help_true

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = {"-c": "config_file", "-d": "config_dir", "-M": True}
        self.func_dict = {"-M": mail_2_rmq.process_message,
                          "-C": mail_2_rmq.check_nonprocess}

    @mock.patch("mail_2_rmq.run_program")
    @mock.patch("mail_2_rmq.gen_libs.help_func")
    @mock.patch("mail_2_rmq.arg_parser")
    def test_dir_chk_crt_false(self, mock_arg, mock_help, mock_run):

        """Function:  test_dir_chk_crt_false

        Description:  Test with arg_dir_chk_crt returns False.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_xor_dict.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_run.return_value = True

        self.assertFalse(mail_2_rmq.main())

    @mock.patch("mail_2_rmq.gen_libs.help_func")
    @mock.patch("mail_2_rmq.arg_parser")
    def test_dir_chk_crt_true(self, mock_arg, mock_help):

        """Function:  test_dir_chk_crt_true

        Description:  Test with arg_dir_chk_crt returns True.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = True
        mock_arg.arg_xor_dict.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = True

        self.assertFalse(mail_2_rmq.main())

    @mock.patch("mail_2_rmq.gen_libs.help_func")
    @mock.patch("mail_2_rmq.arg_parser")
    def test_xor_dict_true(self, mock_arg, mock_help):

        """Function:  test_xor_dict_true

        Description:  Test with arg_xor_dict returns True.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = True
        mock_arg.arg_xor_dict.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = True

        self.assertFalse(mail_2_rmq.main())

    @mock.patch("mail_2_rmq.gen_libs.help_func")
    @mock.patch("mail_2_rmq.arg_parser")
    def test_xor_dict_false(self, mock_arg, mock_help):

        """Function:  test_xor_dict_false

        Description:  Test with arg_xor_dict returns False.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = True
        mock_arg.arg_xor_dict.return_value = False

        self.assertFalse(mail_2_rmq.main())

    @mock.patch("mail_2_rmq.gen_libs.help_func")
    @mock.patch("mail_2_rmq.arg_parser")
    def test_require_false(self, mock_arg, mock_help):

        """Function:  test_require_false

        Description:  Test with arg_require returns False.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = True
        mock_arg.arg_xor_dict.return_value = False

        self.assertFalse(mail_2_rmq.main())

    @mock.patch("mail_2_rmq.gen_libs.help_func")
    @mock.patch("mail_2_rmq.arg_parser")
    def test_require_true(self, mock_arg, mock_help):

        """Function:  test_require_true

        Description:  Test with arg_require returns True.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = True

        self.assertFalse(mail_2_rmq.main())

    @mock.patch("mail_2_rmq.gen_libs.help_func")
    @mock.patch("mail_2_rmq.arg_parser")
    def test_help_false(self, mock_arg, mock_help):

        """Function:  test_status_false

        Description:  Test with help_func returns False.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = True

        self.assertFalse(mail_2_rmq.main())

    @mock.patch("mail_2_rmq.gen_libs.help_func")
    @mock.patch("mail_2_rmq.arg_parser.arg_parse2")
    def test_help_true(self, mock_arg, mock_help):

        """Function:  test_status_true

        Description:  Test with help_func returns True.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_help.return_value = True

        self.assertFalse(mail_2_rmq.main())


if __name__ == "__main__":
    unittest.main()
