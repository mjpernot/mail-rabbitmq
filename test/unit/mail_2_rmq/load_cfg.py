#!/usr/bin/python
# Classification (U)

"""Program:  load_cfg.py

    Description:  Unit testing of load_cfg in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/load_cfg.py

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
        test_false_false_cfg -> Test False and False statuses.
        test_false_true_cfg -> Test False and True statuses.
        test_true_false_cfg -> Test True and False statuses.
        test_true_true_cfg -> Test True and True statuses.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:
            None

        """

        class CfgTest(object):

            """Class:  CfgTest

            Description:  Class which is a representation of a cfg module.

            Super-Class:  object

            Sub-Classes:  None

            Methods:
                __init__ -> Initialize configuration environment.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the CfgTest class.

                Arguments:
                        None

                """

                self.email_dir = "Email_Directory"
                self.log_file = "Log_Directory"

        self.cfg = CfgTest()

        self.cfg_name = "Configuration_File"
        self.cfg_dir = "Configuration_Directory"

    @mock.patch("mail_2_rmq.gen_libs")
    def test_false_false_cfg(self, mock_lib):

        """Function:  test_false_false_cfg

        Description:  Test False and False statuses.

        Arguments:
            None

        """

        mock_lib.load_module.return_value = self.cfg
        mock_lib.chk_crt_dir.side_effect = [[False, ""], [False, ""]]

        self.assertEqual(mail_2_rmq.load_cfg(self.cfg_name, self.cfg_dir),
                         (self.cfg, False))

    @mock.patch("mail_2_rmq.gen_libs")
    def test_false_true_cfg(self, mock_lib):

        """Function:  test_false_true_cfg

        Description:  Test False and True statuses.

        Arguments:
            None

        """

        mock_lib.load_module.return_value = self.cfg
        mock_lib.chk_crt_dir.side_effect = [[False, ""], [True, ""]]

        self.assertEqual(mail_2_rmq.load_cfg(self.cfg_name, self.cfg_dir),
                         (self.cfg, False))

    @mock.patch("mail_2_rmq.gen_libs")
    def test_true_false_cfg(self, mock_lib):

        """Function:  test_true_false_cfg

        Description:  Test True and False statuses.

        Arguments:
            None

        """

        mock_lib.load_module.return_value = self.cfg
        mock_lib.chk_crt_dir.side_effect = [[True, ""], [False, ""]]

        self.assertEqual(mail_2_rmq.load_cfg(self.cfg_name, self.cfg_dir),
                         (self.cfg, False))

    @mock.patch("mail_2_rmq.gen_libs")
    def test_true_true_cfg(self, mock_lib):

        """Function:  test_true_true_cfg

        Description:  Test True and True statuses.

        Arguments:
            None

        """

        mock_lib.load_module.return_value = self.cfg
        mock_lib.chk_crt_dir.side_effect = [[True, ""], [True, ""]]

        self.assertEqual(mail_2_rmq.load_cfg(self.cfg_name, self.cfg_dir),
                         (self.cfg, True))


if __name__ == "__main__":
    unittest.main()
