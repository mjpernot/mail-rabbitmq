#!/usr/bin/python
# Classification (U)

"""Program:  run_program.py

    Description:  Unit testing of run_program in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/run_program.py

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
import lib.gen_libs as gen_libs
import version

# Version
__version__ = version.__version__


def process_message(cfg, LOG, **kwargs):

    """Function:  process_message

    Description:  This is a function stub for mail_2_rmq.process_message.

    Arguments:
        cfg -> Stub argument holder.
        LOG -> Stub argument holder.

    """

    pass


def check_nonprocess(cfg, LOG, **kwargs):

    """Function:  check_nonprocess

    Description:  This is a function stub for mail_2_rmq.check_nonprocess.

    Arguments:
        cfg -> Stub argument holder.
        LOG -> Stub argument holder.

    """

    pass


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Super-Class:  unittest.TestCase

    Sub-Classes:  None

    Methods:
        setUp -> Unit testing initilization.
        test_false_status -> Test with false status flag.

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

                self.log_file = "LOG_FILE"
                self.host = "HOSTNAME"
                self.exchange_name = "EXCHANGE_NAME"
                self.exchange_type = "EXCAHNGE_TYPE"
                self.valid_queues = ["QUEUE1", "QUEUE2"]
                self.email_dir = "EMAIL_DIRECTORY"

        self.cfg = CfgTest()

        self.args_array = {"-c": "CONFIG_FILE", "-d": "CONFIG_DIRECTORY"}
        self.func_dict = {"-M": process_message, "-C": check_nonprocess}

    @mock.patch("mail_2_rmq.load_cfg")
    def test_false_status(self, mock_cfg):

        """Function:  test_false_status

        Description:  Test with false status flag.

        Arguments:
            

        """

        mock_cfg.return_value = (self.cfg, False)

        with gen_libs.no_std_out():
            self.assertFalse(mail_2_rmq.run_program(self.args_array,
                                                    self.func_dict))


if __name__ == "__main__":
    unittest.main()
