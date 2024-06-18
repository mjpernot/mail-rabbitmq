# Classification (U)

"""Program:  connect_process.py

    Description:  Unit testing of connect_process in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/connect_process.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest
import collections
import mock

# Local
sys.path.append(os.getcwd())
import mail_2_rmq
import version

__version__ = version.__version__


class RQTest(object):

    """Class:  RQTest

    Description:  Class which is a representation of a RQ class.

    Methods:
        __init__
        publish_msg

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the RQTest class.

        Arguments:

        """

        self.queue_name = "Test_Queue"
        self.pub_status = True
        self.msg = None

    def publish_msg(self, msg):

        """Method:  publish_msg

        Description:  Stub holder for publish_msg method.

        Arguments:

        """

        self.msg = msg

        return self.pub_status


class CfgTest(object):

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

        self.host = "HOSTNAME"
        self.exchange_name = "EXCHANGE_NAME"
        self.err_queue = "ERROR_QUEUE"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_empty_email
        test_empty_file
        test_file_publish
        test_false_publish
        test_true_publish
        test_error_queue
        test_non_error_queue

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()
        self.rmq = RQTest()
        self.msg = {"from": "FromEmail", "to": "ToEmail",
                    "subject": "EmailSubject"}
        self.text = "EmailBody"
        self.fname = "test/unit/mail_2_rmq/testfiles/fileattachment.txt"
        self.fname2 = "test/unit/mail_2_rmq/testfiles/fileattachment2.txt"

    @mock.patch("mail_2_rmq.get_text")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_error_queue_no_text(self, mock_log, mock_msg):

        """Function:  test_error_queue_no_text

        Description:  Test message sent to error queue with no email text.

        Arguments:

        """

        mock_log.return_value = True
        mock_msg.return_value = None

        self.rmq.queue_name = self.cfg.err_queue

        self.assertFalse(
            mail_2_rmq.connect_process(self.rmq, mock_log, self.cfg, self.msg))

    @mock.patch("mail_2_rmq.archive_email", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.get_text")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_empty_email(self, mock_log, mock_msg):

        """Function:  test_empty_email

        Description:  Test with empty email body.

        Arguments:

        """

        mock_log.return_value = True
        mock_msg.return_value = ""

        self.assertFalse(
            mail_2_rmq.connect_process(self.rmq, mock_log, self.cfg, self.msg))

    @mock.patch("mail_2_rmq.archive_email", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.get_text")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_empty_file(self, mock_log, mock_msg):

        """Function:  test_empty_file

        Description:  Test with empty file passed.

        Arguments:

        """

        mock_log.return_value = True
        mock_msg.return_value = self.text

        self.assertFalse(
            mail_2_rmq.connect_process(
                self.rmq, mock_log, self.cfg, mock_msg, fname=self.fname2))

    @mock.patch("mail_2_rmq.get_text")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_file_publish(self, mock_log, mock_msg):

        """Function:  test_file_publish

        Description:  Test with file name passed.

        Arguments:

        """

        mock_log.return_value = True
        mock_msg.return_value = self.text

        self.assertFalse(
            mail_2_rmq.connect_process(
                self.rmq, mock_log, self.cfg, mock_msg, fname=self.fname))

    @mock.patch("mail_2_rmq.get_text")
    @mock.patch("mail_2_rmq.archive_email")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_false_publish(self, mock_log, mock_archive, mock_msg):

        """Function:  test_false_publish

        Description:  Test publish returns false.

        Arguments:

        """

        mock_log.return_value = True
        mock_archive.return_value = True
        mock_msg.return_value = self.text

        self.rmq.pub_status = False

        self.assertFalse(
            mail_2_rmq.connect_process(self.rmq, mock_log, self.cfg, self.msg))

    @mock.patch("mail_2_rmq.get_text")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_true_publish(self, mock_log, mock_msg):

        """Function:  test_true_publish

        Description:  Test publish returns true.

        Arguments:

        """

        mock_log.return_value = True
        mock_msg.return_value = self.text

        self.assertFalse(
            mail_2_rmq.connect_process(self.rmq, mock_log, self.cfg, self.msg))

    @mock.patch("mail_2_rmq.get_text")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_error_queue(self, mock_log, mock_msg):

        """Function:  test_error_queue

        Description:  Test message sent to error queue.

        Arguments:

        """

        mock_log.return_value = True
        mock_msg.return_value = self.text

        self.rmq.queue_name = self.cfg.err_queue

        self.assertFalse(
            mail_2_rmq.connect_process(self.rmq, mock_log, self.cfg, self.msg))

    @mock.patch("mail_2_rmq.get_text")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_non_error_queue(self, mock_log, mock_msg):

        """Function:  test_non_error_queue

        Description:  Test message sent to non-error queue.

        Arguments:

        """

        mock_log.return_value = True
        mock_msg.return_value = self.text

        self.assertFalse(
            mail_2_rmq.connect_process(self.rmq, mock_log, self.cfg, self.msg))


if __name__ == "__main__":
    unittest.main()
