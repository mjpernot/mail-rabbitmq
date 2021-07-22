#!/usr/bin/python
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

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

# Third-party
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
        create_connection
        publish_msg
        change_channel

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the RQTest class.

        Arguments:

        """

        self.exchange = "Test_Exchange"
        self.queue_name = "Test_Queue"
        self.status = collections.namedtuple("RQ", "is_open")
        self.channel = self.status(True)
        self.conn_status = True
        self.err_msg = ""
        self.pub_status = True
        self.msg = None

    def create_connection(self):

        """Method:  create_connection

        Description:  Stub holder for create_connection method.

        Arguments:

        """

        return self.conn_status, self.err_msg

    def publish_msg(self, msg):

        """Method:  publish_msg

        Description:  Stub holder for publish_msg method.

        Arguments:

        """

        self.msg = msg

        return self.pub_status

    def change_channel(self, stat):

        """Method:  change_channel

        Description:  Change channel status.

        Arguments:

        """

        self.channel = self.status(stat)


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
        test_true_true_connect
        test_false_false_connect
        test_false_true_connect
        test_true_false_connect

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()
        self.rmq = RQTest()
        self.msg = "Email message"
        self.fname = "test/unit/mail_2_rmq/testfiles/fileattachment.txt"
        self.fname2 = "test/unit/mail_2_rmq/testfiles/fileattachment2.txt"

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

        self.assertFalse(mail_2_rmq.connect_process(self.rmq, mock_log,
                                                    self.cfg, mock_msg))

    @mock.patch("mail_2_rmq.archive_email", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.get_text")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_empty_file(self, mock_log, mock_msg):

        """Function:  test_empty_file

        Description:  Test with empty file passed.

        Arguments:

        """

        mock_log.return_value = True
        mock_msg.return_value = self.msg

        self.assertFalse(
            mail_2_rmq.connect_process(self.rmq, mock_log, self.cfg,
                                       mock_msg, fname=self.fname2))

    @mock.patch("mail_2_rmq.get_text")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_file_publish(self, mock_log, mock_msg):

        """Function:  test_file_publish

        Description:  Test with file name passed.

        Arguments:

        """

        mock_log.return_value = True
        mock_msg.return_value = self.msg

        self.assertFalse(
            mail_2_rmq.connect_process(self.rmq, mock_log, self.cfg,
                                       mock_msg, fname=self.fname))

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
        mock_msg.return_value = self.msg

        self.rmq.pub_status = False

        self.assertFalse(mail_2_rmq.connect_process(self.rmq, mock_log,
                                                    self.cfg, mock_msg))

    @mock.patch("mail_2_rmq.get_text")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_true_publish(self, mock_log, mock_msg):

        """Function:  test_true_publish

        Description:  Test publish returns true.

        Arguments:

        """

        mock_log.return_value = True
        mock_msg.return_value = self.msg

        self.assertFalse(mail_2_rmq.connect_process(self.rmq, mock_log,
                                                    self.cfg, mock_msg))

    @mock.patch("mail_2_rmq.get_text")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_error_queue(self, mock_log, mock_msg):

        """Function:  test_error_queue

        Description:  Test message sent to error queue.

        Arguments:

        """

        mock_log.return_value = True
        mock_msg.return_value = self.msg

        self.rmq.queue_name = self.cfg.err_queue

        self.assertFalse(mail_2_rmq.connect_process(self.rmq, mock_log,
                                                    self.cfg, mock_msg))

    @mock.patch("mail_2_rmq.get_text")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_non_error_queue(self, mock_log, mock_msg):

        """Function:  test_non_error_queue

        Description:  Test message sent to non-error queue.

        Arguments:

        """

        mock_log.return_value = True
        mock_msg.return_value = self.msg

        self.assertFalse(mail_2_rmq.connect_process(self.rmq, mock_log,
                                                    self.cfg, mock_msg))

    @mock.patch("mail_2_rmq.get_text")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_true_true_connect(self, mock_log, mock_msg):

        """Function:  test_true_true_connect

        Description:  Test connecting to RabbitMQ with true/true status.

        Arguments:

        """

        mock_log.return_value = True
        mock_msg.return_value = self.msg

        self.assertFalse(mail_2_rmq.connect_process(self.rmq, mock_log,
                                                    self.cfg, mock_msg))

    @mock.patch("mail_2_rmq.archive_email")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_false_false_connect(self, mock_log, mock_archive):

        """Function:  test_false_false_connect

        Description:  Test connecting to RabbitMQ with false/false status.

        Arguments:

        """

        mock_log.return_value = True
        mock_archive.return_value = True

        self.rmq.conn_status = False
        self.rmq.change_channel(False)
        self.assertFalse(mail_2_rmq.connect_process(self.rmq, mock_log,
                                                    self.cfg, ""))

    @mock.patch("mail_2_rmq.archive_email")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_false_true_connect(self, mock_log, mock_archive):

        """Function:  test_false_true_connect

        Description:  Test connecting to RabbitMQ with false/true status.

        Arguments:

        """

        mock_log.return_value = True
        mock_archive.return_value = True

        self.rmq.conn_status = False
        self.assertFalse(mail_2_rmq.connect_process(self.rmq, mock_log,
                                                    self.cfg, ""))

    @mock.patch("mail_2_rmq.archive_email")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_true_false_connect(self, mock_log, mock_archive):

        """Function:  test_true_false_connect

        Description:  Test connecting to RabbitMQ with true/false status.

        Arguments:

        """

        mock_log.return_value = True
        mock_archive.return_value = True

        self.rmq.change_channel(False)
        self.assertFalse(mail_2_rmq.connect_process(self.rmq, mock_log,
                                                    self.cfg, ""))


if __name__ == "__main__":
    unittest.main()
