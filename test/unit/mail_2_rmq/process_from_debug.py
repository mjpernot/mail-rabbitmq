# Classification (U)

"""Program:  process_from_debug.py

    Description:  Unit testing of process_from_debug in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/process_from_debug.py

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
        self.queue_dict_debug = {"From Line": "QueueName"}
        self.err_addr_queue = "ERROR_ADDR_QUEUE"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_no_file
        test_rm_fail
        test_valid_from
        test_true_true_connect2
        test_true_true_connect
        test_false_false_connect2
        test_false_false_connect
        test_false_true_connect2
        test_false_true_connect
        test_true_false_connect2
        test_true_false_connect

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()
        self.rmq = Rmq()
        self.subj = "SubjectLine"
        self.msg = "Message Body"
        self.from_addr = "From Line"
        self.fname_list = ["Fname"]
        self.fname_list2 = ["Fname", "Fname2"]
        self.fname_list3 = [
            "test/unit/mail_2_rmq/testfiles/fileattachment.txt"]

    @mock.patch("mail_2_rmq.connect_process_debug",
                mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.gen_libs.rm_file")
    @mock.patch("mail_2_rmq.process_attach_debug")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_multiple_files(self, mock_rmq, mock_log, mock_attch, mock_rm):

        """Function:  test_multiple_files

        Description:  Test with multiple file attachments detected.

        Arguments:

        """

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_attch.return_value = self.fname_list2
        mock_rm.return_value = (False, None)

        self.assertFalse(
            mail_2_rmq.process_from_debug(
                self.cfg, mock_log, self.msg, self.from_addr))

    @mock.patch("mail_2_rmq.connect_process_debug",
                mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.process_attach_debug")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_no_file(self, mock_rmq, mock_log, mock_attch):

        """Function:  test_no_file

        Description:  Test with no file attachment detected.

        Arguments:

        """

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_attch.return_value = []

        self.assertFalse(
            mail_2_rmq.process_from_debug(
                self.cfg, mock_log, self.msg, self.from_addr))

    @mock.patch("mail_2_rmq.connect_process_debug",
                mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.process_attach_debug")
    @mock.patch("mail_2_rmq.gen_libs.rm_file")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_rm_fail(self, mock_rmq, mock_log, mock_rm, mock_attch):

        """Function:  test_rm_fail

        Description:  Test with removal file failure.

        Arguments:

        """

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_rm.return_value = (True, "Error Message")
        mock_attch.return_value = self.fname_list3

        self.assertFalse(
            mail_2_rmq.process_from_debug(
                self.cfg, mock_log, self.msg, self.from_addr))

    @mock.patch("mail_2_rmq.connect_process_debug",
                mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.process_attach_debug")
    @mock.patch("mail_2_rmq.gen_libs.rm_file")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_valid_from(self, mock_rmq, mock_log, mock_rm, mock_attch):

        """Function:  test_valid_from

        Description:  Test email with valid from line and file.

        Arguments:

        """

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_rm.return_value = (False, None)
        mock_attch.return_value = self.fname_list

        self.assertFalse(
            mail_2_rmq.process_from_debug(
                self.cfg, mock_log, self.msg, self.from_addr))

    @mock.patch("mail_2_rmq.connect_process_debug",
                mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.process_attach_debug")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_true_true_connect2(self, mock_rmq, mock_log, mock_attch):

        """Function:  test_true_true_connect2

        Description:  Test connecting to RabbitMQ with true/true status.

        Arguments:

        """

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_attch.return_value = []

        self.assertFalse(
            mail_2_rmq.process_from_debug(
                self.cfg, mock_log, self.msg, self.from_addr))

    @mock.patch("mail_2_rmq.connect_process_debug",
                mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.process_attach_debug")
    @mock.patch("mail_2_rmq.gen_libs.rm_file")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_true_true_connect(self, mock_rmq, mock_log, mock_rm, mock_attch):

        """Function:  test_true_true_connect

        Description:  Test connecting to RabbitMQ with true/true status.

        Arguments:

        """

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_rm.return_value = (False, None)
        mock_attch.return_value = self.fname_list

        self.assertFalse(
            mail_2_rmq.process_from_debug(
                self.cfg, mock_log, self.msg, self.from_addr))

    @mock.patch("mail_2_rmq.process_attach_debug")
    @mock.patch("mail_2_rmq.archive_email_debug")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_false_false_connect2(self, mock_rmq, mock_log, mock_archive,
                                  mock_attch):

        """Function:  test_false_false_connect2

        Description:  Test connecting to RabbitMQ with false/false status.

        Arguments:

        """

        self.rmq.conn_status = False
        self.rmq.change_channel(False)

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_archive.return_value = True
        mock_attch.return_value = []

        self.assertFalse(
            mail_2_rmq.process_from_debug(
                self.cfg, mock_log, self.msg, self.from_addr))

    @mock.patch("mail_2_rmq.process_attach_debug")
    @mock.patch("mail_2_rmq.gen_libs.rm_file")
    @mock.patch("mail_2_rmq.archive_email_debug")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_false_false_connect(               # pylint:disable=R0913,R0917
            self, mock_rmq, mock_log, mock_archive, mock_rm, mock_attch):

        """Function:  test_false_false_connect

        Description:  Test connecting to RabbitMQ with false/false status.

        Arguments:

        """

        self.rmq.conn_status = False
        self.rmq.change_channel(False)

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_archive.return_value = True
        mock_rm.return_value = (False, None)
        mock_attch.return_value = self.fname_list

        self.assertFalse(
            mail_2_rmq.process_from_debug(
                self.cfg, mock_log, self.msg, self.from_addr))

    @mock.patch("mail_2_rmq.process_attach_debug")
    @mock.patch("mail_2_rmq.archive_email_debug")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_false_true_connect2(self, mock_rmq, mock_log, mock_archive,
                                 mock_attch):

        """Function:  test_false_true_connect2

        Description:  Test connecting to RabbitMQ with false/true status.

        Arguments:

        """

        self.rmq.conn_status = False

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_archive.return_value = True
        mock_attch.return_value = []

        self.assertFalse(
            mail_2_rmq.process_from_debug(
                self.cfg, mock_log, self.msg, self.from_addr))

    @mock.patch("mail_2_rmq.process_attach_debug")
    @mock.patch("mail_2_rmq.gen_libs.rm_file")
    @mock.patch("mail_2_rmq.archive_email_debug")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_false_true_connect(                # pylint:disable=R0913,R0917
            self, mock_rmq, mock_log, mock_archive, mock_rm, mock_attch):

        """Function:  test_false_true_connect

        Description:  Test connecting to RabbitMQ with false/true status.

        Arguments:

        """

        self.rmq.conn_status = False

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_archive.return_value = True
        mock_rm.return_value = (False, None)
        mock_attch.return_value = self.fname_list

        self.assertFalse(
            mail_2_rmq.process_from_debug(
                self.cfg, mock_log, self.msg, self.from_addr))

    @mock.patch("mail_2_rmq.process_attach_debug")
    @mock.patch("mail_2_rmq.archive_email_debug")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_true_false_connect2(self, mock_rmq, mock_log, mock_archive,
                                 mock_attch):

        """Function:  test_true_false_connect2

        Description:  Test connecting to RabbitMQ with true/false status.

        Arguments:

        """

        self.rmq.change_channel(False)

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_archive.return_value = True
        mock_attch.return_value = []

        self.assertFalse(
            mail_2_rmq.process_from_debug(
                self.cfg, mock_log, self.msg, self.from_addr))

    @mock.patch("mail_2_rmq.process_attach_debug")
    @mock.patch("mail_2_rmq.gen_libs.rm_file")
    @mock.patch("mail_2_rmq.archive_email_debug")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_true_false_connect(                # pylint:disable=R0913,R0917
            self, mock_rmq, mock_log, mock_archive, mock_rm, mock_attch):

        """Function:  test_true_false_connect

        Description:  Test connecting to RabbitMQ with true/false status.

        Arguments:

        """

        self.rmq.change_channel(False)

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_archive.return_value = True
        mock_rm.return_value = (False, None)
        mock_attch.return_value = self.fname_list

        self.assertFalse(
            mail_2_rmq.process_from_debug(
                self.cfg, mock_log, self.msg, self.from_addr))


if __name__ == "__main__":
    unittest.main()
