# Classification (U)

"""Program:  connect_rmq.py

    Description:  Unit testing of connect_rmq in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/connect_rmq.py

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
import mail_2_rmq                               # pylint:disable=E0401,C0413
import version                                  # pylint:disable=C0413,E0401

__version__ = version.__version__


class Rmq():

    """Class:  Rmq

    Description:  Class which is a representation of the
        rabbitmq_class.RabbitMQPub class.

    Methods:
        __init__
        create_connection
        close
        change_channel

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the CfgTest class.

        Arguments:

        """

        self.status = collections.namedtuple("RQ", "is_open")
        self.channel = self.status(True)
        self.conn_status = True
        self.err_msg = ""

    def create_connection(self):

        """Method:  create_connection

        Description:  Stub holder for create_connection method.

        Arguments:

        """

        return self.conn_status, self.err_msg

    def close(self):

        """Method:  close

        Description:  Close the RMQ connection.

        Arguments:

        """

    def change_channel(self, stat):

        """Method:  change_channel

        Description:  Change channel status.

        Arguments:

        """

        self.channel = self.status(stat)


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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_filname
        test_no_filname
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
        self.rmq = Rmq()
        self.qname = "QueueName"
        self.rkey = "RKey"
        self.msg = "Message Body"
        self.fname = "AttachementFilename"

    @mock.patch("mail_2_rmq.connect_process", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_filname(self, mock_rmq, mock_log):

        """Function:  test_filname

        Description:  Test with filename passed.

        Arguments:

        """

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True

        self.assertFalse(
            mail_2_rmq.connect_rmq(
                self.cfg, mock_log, self.qname, self.rkey, self.msg,
                fname=self.fname))

    @mock.patch("mail_2_rmq.connect_process", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_no_filname(self, mock_rmq, mock_log):

        """Function:  test_no_filname

        Description:  Test with no filename passed.

        Arguments:

        """

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True

        self.assertFalse(
            mail_2_rmq.connect_rmq(
                self.cfg, mock_log, self.qname, self.rkey, self.msg))

    @mock.patch("mail_2_rmq.connect_process", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_true_true_connect(self, mock_rmq, mock_log):

        """Function:  test_true_true_connect

        Description:  Test connecting to RabbitMQ with true/true status.

        Arguments:

        """

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True

        self.assertFalse(
            mail_2_rmq.connect_rmq(
                self.cfg, mock_log, self.qname, self.rkey, self.msg))

    @mock.patch("mail_2_rmq.archive_email")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_false_false_connect(self, mock_rmq, mock_log, mock_archive):

        """Function:  test_false_false_connect

        Description:  Test connecting to RabbitMQ with false/false status.

        Arguments:

        """

        self.rmq.conn_status = False
        self.rmq.change_channel(False)

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_archive.return_value = True

        self.assertFalse(
            mail_2_rmq.connect_rmq(
                self.cfg, mock_log, self.qname, self.rkey, self.msg))

    @mock.patch("mail_2_rmq.archive_email")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_false_true_connect(self, mock_rmq, mock_log, mock_archive):

        """Function:  test_false_true_connect

        Description:  Test connecting to RabbitMQ with false/true status.

        Arguments:

        """

        self.rmq.conn_status = False

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_archive.return_value = True

        self.assertFalse(
            mail_2_rmq.connect_rmq(
                self.cfg, mock_log, self.qname, self.rkey, self.msg))

    @mock.patch("mail_2_rmq.archive_email")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_true_false_connect(self, mock_rmq, mock_log, mock_archive):

        """Function:  test_true_false_connect

        Description:  Test connecting to RabbitMQ with true/false status.

        Arguments:

        """

        self.rmq.change_channel(False)

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_archive.return_value = True

        self.assertFalse(
            mail_2_rmq.connect_rmq(
                self.cfg, mock_log, self.qname, self.rkey, self.msg))


if __name__ == "__main__":
    unittest.main()
