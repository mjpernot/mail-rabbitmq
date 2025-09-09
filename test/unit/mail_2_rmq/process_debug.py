# Classification (U)

"""Program:  process_debug.py

    Description:  Unit testing of process_debug in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/process_debug.py

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


class LoggerTest():

    """Class:  LoggerTest

    Description:  Class which is a representation of a Logger class.

    Methods:
        __init__
        log_debug
        log_info
        log_close

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the LoggerTest class.

        Arguments:

        """

        self.data = None

    def log_debug(self, data):

        """Method:  log_debug

        Description:  Stub holder for Logger.log_debug method.

        Arguments:

        """

        self.data = data

    def log_info(self, data):

        """Method:  log_info

        Description:  Stub holder for Logger.log_info method.

        Arguments:

        """

        self.data = data

    def log_close(self):

        """Method:  log_close

        Description:  Stub holder for Logger.log_close method.

        Arguments:

        """


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

        self.user = "USERNAME"
        self.japd = "JAPD"
        self.host = "HOSTNAME"
        self.port = 1111
        self.exchange_name = "EXCHANGE_NAME"
        self.exchange_type = "EXCAHNGE_TYPE"
        self.x_durable = True
        self.q_durable = True
        self.auto_delete = True
        self.err_queue = "ERROR_QUEUE"
        self.valid_queues = ["Queue1", "Queue2"]
        self.subj_filter = [r"\[.*\]"]
        self.tmp_dir = "test/unit/mail_2_rmq/tmp"
        self.attach_types = ["application/pdf"]
        self.file_queues = ["FileQueue1", "FileQueue2"]
        self.err_file_queue = "ERROR_FILE_QUEUE"
        self.log_file = "/Path/Log_File.log"
        self.email_dir = "EMAIL_DIRECTORY"
        self.queue_dict = {"goodname@domain": "AddrQueue",
                           "goodname2@domain": "AddrQueue2"}
        self.debug_address = "debug@debug.domain"
        self.debug_valid_queues = ["DebugQueue"]
        self.debug_queue_dict = {"debug_name@domain": "DebugQueue"}


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_attach
        test_from_addr
        test_invalid_subj
        test_valid_subj

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()
        self.log = LoggerTest()
        self.subj = "DebugQueue"
        self.subj2 = "DebugQueue2"
        self.msg = {"subject": "DebugQueue", "from": "From: debug_name@domain"}
        self.from_addr = "debug_name@domain"
        self.from_addr2 = "debug_name@domain2"

    @mock.patch("mail_2_rmq.process_file_debug", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.gen_class")
    def test_attach(self, mock_log):

        """Function:  test_attach

        Description:  Test email with attached file.

        Arguments:

        """

        mock_log.Logger.return_value = self.log

        self.assertFalse(
            mail_2_rmq.process_debug(
                self.cfg, self.subj2, self.msg, self.from_addr2))

    @mock.patch("mail_2_rmq.process_from_debug", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.gen_class")
    def test_from_addr(self, mock_log):

        """Function:  test_from_addr

        Description:  Test email with valid from address.

        Arguments:

        """

        mock_log.Logger.return_value = self.log

        self.assertFalse(
            mail_2_rmq.process_debug(
                self.cfg, self.subj2, self.msg, self.from_addr))

    @mock.patch("mail_2_rmq.process_file_debug", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.gen_class")
    def test_invalid_subj(self, mock_log):

        """Function:  test_invalid_subj

        Description:  Test email with invalid subject.

        Arguments:

        """

        mock_log.Logger.return_value = self.log

        self.assertFalse(
            mail_2_rmq.process_debug(
                self.cfg, self.subj2, self.msg, self.from_addr2))

    @mock.patch("mail_2_rmq.process_subj_debug", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.gen_class")
    def test_valid_subj(self, mock_log):

        """Function:  test_valid_subj

        Description:  Test email with valid subject.

        Arguments:

        """

        mock_log.Logger.return_value = self.log

        self.assertFalse(
            mail_2_rmq.process_debug(
                self.cfg, self.subj, self.msg, self.from_addr))


if __name__ == "__main__":
    unittest.main()
