# Classification (U)

"""Program:  capture_email.py

    Description:  Unit testing of capture_email in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/capture_email.py

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
        self.log_file = "LOG_FILE"
        self.email_dir = "EMAIL_DIRECTORY"
        self.queue_dict = {"goodname@domain": "AddrQueue",
                           "goodname2@domain": "AddrQueue2"}
        self.debug_address = "debug@debug.domain"


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
        test_capture_email

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.raw_msg = ["Raw", "Email", "Message"]
        self.part = ParserTest()
        self.cfg = CfgTest()
        self.processed_msg = "RawEmailMessage"

    @mock.patch("mail_2_rmq.process_message", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.Parser")
    @mock.patch("mail_2_rmq.sys.stdin")
    def test_capture_email(self, mock_stdin, mock_parse, mock_log):

        """Function:  test_capture_email

        Description:  Test parsing an email.

        Arguments:

        """

        mock_parse.return_value = self.part
        mock_stdin.readlines.return_value = self.raw_msg
        mock_log.return_value = True

        self.assertFalse(mail_2_rmq.capture_email(self.cfg, mock_log))


if __name__ == "__main__":
    unittest.main()
