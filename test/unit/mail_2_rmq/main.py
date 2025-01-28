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
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import mail_2_rmq                               # pylint:disable=E0401,C0413
import version                                  # pylint:disable=C0413,E0401

__version__ = version.__version__


class ArgParser():

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        arg_dir_chk
        arg_require
        arg_xor_dict
        arg_parse2

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = {}
        self.opt_req = None
        self.opt_req2 = True
        self.dir_perms_chk = None
        self.dir_perms_chk2 = True
        self.opt_xor_val = None
        self.opt_xor_val2 = True
        self.argparse2 = True

    def arg_dir_chk(self, dir_perms_chk):

        """Method:  arg_dir_chk

        Description:  Method stub holder for gen_class.ArgParser.arg_dir_chk.

        Arguments:

        """

        self.dir_perms_chk = dir_perms_chk

        return self.dir_perms_chk2

    def arg_require(self, opt_req):

        """Method:  arg_require

        Description:  Method stub holder for gen_class.ArgParser.arg_require.

        Arguments:

        """

        self.opt_req = opt_req

        return self.opt_req2

    def arg_xor_dict(self, opt_xor_val):

        """Method:  arg_xor_dict

        Description:  Method stub holder for gen_class.ArgParser.arg_xor_dict.

        Arguments:

        """

        self.opt_xor_val = opt_xor_val

        return self.opt_xor_val2

    def arg_parse2(self):

        """Method:  arg_parse2

        Description:  Method stub holder for gen_class.ArgParser.arg_parse2.

        Arguments:

        """

        return self.argparse2


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_arg_parse2_false
        test_arg_parse2_true
        test_help_true
        test_help_false
        test_require_false
        test_require_true
        test_xor_dict_false
        test_xor_dict_true
        test_dir_chk_crt_false
        test_dir_chk_crt_true

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.args.args_array = {
            "-c": "config_file", "-d": "config_dir", "-M": True}

    @mock.patch("mail_2_rmq.gen_libs.help_func")
    @mock.patch("mail_2_rmq.gen_class.ArgParser")
    def test_arg_parse2_false(self, mock_arg, mock_help):

        """Function:  test_arg_parse2_false

        Description:  Test arg_parse2 returns false.

        Arguments:

        """

        self.args.argparse2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = True

        self.assertFalse(mail_2_rmq.main())

    @mock.patch("mail_2_rmq.gen_libs.help_func")
    @mock.patch("mail_2_rmq.gen_class.ArgParser")
    def test_help_true(self, mock_arg, mock_help):

        """Function:  test_status_true

        Description:  Test with help_func returns True.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_help.return_value = True

        self.assertFalse(mail_2_rmq.main())

    @mock.patch("mail_2_rmq.gen_libs.help_func")
    @mock.patch("mail_2_rmq.gen_class.ArgParser")
    def test_help_false(self, mock_arg, mock_help):

        """Function:  test_status_false

        Description:  Test with help_func returns False.

        Arguments:

        """

        self.args.opt_req2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(mail_2_rmq.main())

    @mock.patch("mail_2_rmq.gen_libs.help_func")
    @mock.patch("mail_2_rmq.gen_class.ArgParser")
    def test_require_false(self, mock_arg, mock_help):

        """Function:  test_require_false

        Description:  Test with arg_require returns False.

        Arguments:

        """

        self.args.opt_req2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(mail_2_rmq.main())

    @mock.patch("mail_2_rmq.gen_libs.help_func")
    @mock.patch("mail_2_rmq.gen_class.ArgParser")
    def test_require_true(self, mock_arg, mock_help):

        """Function:  test_require_true

        Description:  Test with arg_require returns True.

        Arguments:

        """

        self.args.opt_xor_val2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(mail_2_rmq.main())

    @mock.patch("mail_2_rmq.gen_libs.help_func")
    @mock.patch("mail_2_rmq.gen_class.ArgParser")
    def test_xor_dict_false(self, mock_arg, mock_help):

        """Function:  test_xor_dict_false

        Description:  Test with arg_xor_dict returns False.

        Arguments:

        """

        self.args.opt_xor_val2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(mail_2_rmq.main())

    @mock.patch("mail_2_rmq.gen_libs.help_func")
    @mock.patch("mail_2_rmq.gen_class.ArgParser")
    def test_xor_dict_true(self, mock_arg, mock_help):

        """Function:  test_xor_dict_true

        Description:  Test with arg_xor_dict returns True.

        Arguments:

        """

        self.args.dir_perms_chk2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(mail_2_rmq.main())

    @mock.patch("mail_2_rmq.gen_libs.help_func")
    @mock.patch("mail_2_rmq.gen_class.ArgParser")
    def test_dir_chk_crt_false(self, mock_arg, mock_help):

        """Function:  test_dir_chk_crt_false

        Description:  Test with arg_dir_chk_crt returns False.

        Arguments:

        """

        self.args.dir_perms_chk2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(mail_2_rmq.main())

    @mock.patch("mail_2_rmq.run_program", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.gen_libs.help_func")
    @mock.patch("mail_2_rmq.gen_class.ArgParser")
    def test_dir_chk_crt_true(self, mock_arg, mock_help):

        """Function:  test_dir_chk_crt_true

        Description:  Test with arg_dir_chk_crt returns True.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(mail_2_rmq.main())

    @mock.patch("mail_2_rmq.run_program", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.gen_libs.help_func")
    @mock.patch("mail_2_rmq.gen_class.ArgParser")
    def test_run_program(self, mock_arg, mock_help):

        """Function:  test_run_program

        Description:  Test with run_program.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(mail_2_rmq.main())


if __name__ == "__main__":
    unittest.main()
