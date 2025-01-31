# Classification (U)

"""Program:  load_cfg.py

    Description:  Unit testing of load_cfg in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/load_cfg.py

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


class CfgTest():                                        # pylint:disable=R0903

    """Class:  CfgTest

    Description:  Class which is a representation of a cfg module.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the CfgTest class.

        Arguments:

        """

        self.email_dir = "Email_Directory"
        self.log_file = "Log_Directory"
        self.tmp_dir = "Tmp_Directory"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_tmp_dir_false
        test_tmp_dir_true
        test_log_file_false
        test_log_file_true
        test_email_dir_false
        test_email_dir_true
        test_false_false_cfg
        test_false_true_cfg
        test_true_false_cfg
        test_true_true_cfg

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()
        self.cfg_name = "Configuration_File"
        self.cfg_dir = "Configuration_Directory"
        self.results = [[True, ""], [True, ""], [True, ""]]
        self.results2 = [[False, "Err1"], [False, "Err2"], [False, "Err3"]]
        self.results3 = [[False, "Err1"], [True, ""], [True, ""]]
        self.results4 = [[True, ""], [False, "Err2"], [True, ""]]
        self.results5 = [[True, ""], [True, ""], [False, "Err3"]]
        self.err_results = ["Err1", "Err2", "Err3"]
        self.err_results2 = ["Err1"]
        self.err_results3 = ["Err2"]
        self.err_results4 = ["Err3"]

    @mock.patch("mail_2_rmq.gen_libs")
    def test_tmp_dir_false(self, mock_lib):

        """Function:  test_tmp_dir_false

        Description:  Test with tmp_dir check failure.

        Arguments:

        """

        mock_lib.load_module.return_value = self.cfg
        mock_lib.chk_crt_dir.side_effect = self.results5

        self.assertEqual(mail_2_rmq.load_cfg(self.cfg_name, self.cfg_dir),
                         (self.cfg, False, self.err_results4))

    @mock.patch("mail_2_rmq.gen_libs")
    def test_tmp_dir_true(self, mock_lib):

        """Function:  test_tmp_dir_true

        Description:  Test with tmp_dir check success.

        Arguments:

        """

        mock_lib.load_module.return_value = self.cfg
        mock_lib.chk_crt_dir.side_effect = self.results

        self.assertEqual(mail_2_rmq.load_cfg(self.cfg_name, self.cfg_dir),
                         (self.cfg, True, []))

    @mock.patch("mail_2_rmq.gen_libs")
    def test_log_file_false(self, mock_lib):

        """Function:  test_log_file_false

        Description:  Test with log_file check failure.

        Arguments:

        """

        mock_lib.load_module.return_value = self.cfg
        mock_lib.chk_crt_dir.side_effect = self.results4

        self.assertEqual(mail_2_rmq.load_cfg(self.cfg_name, self.cfg_dir),
                         (self.cfg, False, self.err_results3))

    @mock.patch("mail_2_rmq.gen_libs")
    def test_log_file_true(self, mock_lib):

        """Function:  test_log_file_true

        Description:  Test with log_file check success.

        Arguments:

        """

        mock_lib.load_module.return_value = self.cfg
        mock_lib.chk_crt_dir.side_effect = self.results

        self.assertEqual(mail_2_rmq.load_cfg(self.cfg_name, self.cfg_dir),
                         (self.cfg, True, []))

    @mock.patch("mail_2_rmq.gen_libs")
    def test_email_dir_false(self, mock_lib):

        """Function:  test_email_dir_false

        Description:  Test with email_dir check failure.

        Arguments:

        """

        mock_lib.load_module.return_value = self.cfg
        mock_lib.chk_crt_dir.side_effect = self.results3

        self.assertEqual(mail_2_rmq.load_cfg(self.cfg_name, self.cfg_dir),
                         (self.cfg, False, self.err_results2))

    @mock.patch("mail_2_rmq.gen_libs")
    def test_email_dir_true(self, mock_lib):

        """Function:  test_email_dir_true

        Description:  Test with email_dir check success.

        Arguments:

        """

        mock_lib.load_module.return_value = self.cfg
        mock_lib.chk_crt_dir.side_effect = self.results

        self.assertEqual(mail_2_rmq.load_cfg(self.cfg_name, self.cfg_dir),
                         (self.cfg, True, []))

    @mock.patch("mail_2_rmq.gen_libs")
    def test_false_false_cfg(self, mock_lib):

        """Function:  test_false_false_cfg

        Description:  Test False and False statuses.

        Arguments:

        """

        mock_lib.load_module.return_value = self.cfg
        mock_lib.chk_crt_dir.side_effect = self.results2

        self.assertEqual(mail_2_rmq.load_cfg(self.cfg_name, self.cfg_dir),
                         (self.cfg, False, self.err_results))

    @mock.patch("mail_2_rmq.gen_libs")
    def test_false_true_cfg(self, mock_lib):

        """Function:  test_false_true_cfg

        Description:  Test False and True statuses.

        Arguments:

        """

        mock_lib.load_module.return_value = self.cfg
        mock_lib.chk_crt_dir.side_effect = self.results3

        self.assertEqual(mail_2_rmq.load_cfg(self.cfg_name, self.cfg_dir),
                         (self.cfg, False, self.err_results2))

    @mock.patch("mail_2_rmq.gen_libs")
    def test_true_false_cfg(self, mock_lib):

        """Function:  test_true_false_cfg

        Description:  Test True and False statuses.

        Arguments:

        """

        mock_lib.load_module.return_value = self.cfg
        mock_lib.chk_crt_dir.side_effect = self.results4

        self.assertEqual(mail_2_rmq.load_cfg(self.cfg_name, self.cfg_dir),
                         (self.cfg, False, self.err_results3))

    @mock.patch("mail_2_rmq.gen_libs")
    def test_true_true_cfg(self, mock_lib):

        """Function:  test_true_true_cfg

        Description:  Test True and True statuses.

        Arguments:

        """

        mock_lib.load_module.return_value = self.cfg
        mock_lib.chk_crt_dir.side_effect = self.results

        self.assertEqual(mail_2_rmq.load_cfg(self.cfg_name, self.cfg_dir),
                         (self.cfg, True, []))


if __name__ == "__main__":
    unittest.main()
