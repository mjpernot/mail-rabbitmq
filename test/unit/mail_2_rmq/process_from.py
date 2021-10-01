#!/usr/bin/python
# Classification (U)

"""Program:  process_from.py

    Description:  Unit testing of process_from in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/process_from.py

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
import mock

# Local
sys.path.append(os.getcwd())
import mail_2_rmq
import version

__version__ = version.__version__


class Rmq(object):

    """Class:  Rmq

    Description:  Class which is a representation of the
        rabbitmq_class.RabbitMQPub class.

    Methods:
        __init__
        close

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the CfgTest class.

        Arguments:

        """

        pass

    def close(self):

        """Method:  close

        Description:  Close the RMQ connection.

        Arguments:

        """

        pass


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
        self.queue_dict = {"From Line": "QueueName"}
        self.err_addr_queue = "ERROR_ADDR_QUEUE"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_no_file
        test_rm_fail
        test_valid_from

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

    @mock.patch("mail_2_rmq.connect_process", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.process_attach")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_multiple_files(self, mock_rmq, mock_log, mock_attch):

        """Function:  test_multiple_files

        Description:  Test with multiple file attachments detected.

        Arguments:

        """

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_attch.return_value = self.fname_list2

        self.assertFalse(
            mail_2_rmq.process_from(
                self.cfg, mock_log, self.msg, self.from_addr))

    @mock.patch("mail_2_rmq.connect_process", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.process_attach")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_no_file(self, mock_rmq, mock_log, mock_attch):

        """Function:  test_no_file

        Description:  Test with no file attachment detected.

        Arguments:

        """

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_attch.return_value = list()

        self.assertFalse(
            mail_2_rmq.process_from(
                self.cfg, mock_log, self.msg, self.from_addr))

    @mock.patch("mail_2_rmq.connect_process", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.process_attach")
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
        mock_attch.return_value = self.fname_list

        self.assertFalse(
            mail_2_rmq.process_from(
                self.cfg, mock_log, self.msg, self.from_addr))

    @mock.patch("mail_2_rmq.connect_process", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.process_attach")
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
            mail_2_rmq.process_from(
                self.cfg, mock_log, self.msg, self.from_addr))


if __name__ == "__main__":
    unittest.main()
