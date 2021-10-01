#!/usr/bin/python
# Classification (U)

"""Program:  process_file.py

    Description:  Unit testing of process_file in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/process_file.py

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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_invalid_subj_no_file
        test_invalid_subj_multiple_file
        test_valid_subj_multiple_file
        test_invalid_subj
        test_invalid_subj_file_err
        test_invalid_subj_file
        test_valid_subj_file_err
        test_valid_subj

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()
        self.rmq = Rmq()
        self.subj = "FileQueue1"
        self.subj2 = "InvalidSubject"
        self.msg = "Message Body"
        self.from_addr = "From Line"
        self.fname_list = ["Fname"]
        self.fname_list2 = ["Fname", "Fname2"]

    @mock.patch("mail_2_rmq.connect_process", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.process_attach")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_invalid_subj_no_file(self, mock_rmq, mock_log, mock_attch):

        """Function:  test_invalid_subj_no_file

        Description:  Test with invalid subject and no file.

        Arguments:

        """

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_attch.return_value = list()

        self.assertFalse(
            mail_2_rmq.process_file(self.cfg, mock_log, self.subj, self.msg))

    @mock.patch("mail_2_rmq.connect_process", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.process_attach")
    @mock.patch("mail_2_rmq.gen_libs.rm_file")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_invalid_subj_multiple_file(self, mock_rmq, mock_log, mock_rm,
                                        mock_attch):

        """Function:  test_invalid_subj_multiple_file

        Description:  Test with invalid subject and with multiple file
            attachments.

        Arguments:

        """

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_rm.return_value = (False, None)
        mock_attch.return_value = self.fname_list2

        self.assertFalse(
            mail_2_rmq.process_file(self.cfg, mock_log, self.subj2, self.msg))

    @mock.patch("mail_2_rmq.connect_process", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.process_attach")
    @mock.patch("mail_2_rmq.gen_libs.rm_file")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_valid_subj_multiple_file(self, mock_rmq, mock_log, mock_rm,
                                      mock_attch):

        """Function:  test_valid_subj_multiple_file

        Description:  Test email with valid subj and multiple file
            attachments.

        Arguments:

        """

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_rm.return_value = (False, None)
        mock_attch.return_value = self.fname_list2

        self.assertFalse(
            mail_2_rmq.process_file(self.cfg, mock_log, self.subj, self.msg))

    @mock.patch("mail_2_rmq.connect_process", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.process_attach")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_invalid_subj(self, mock_rmq, mock_log, mock_attch):

        """Function:  test_invalid_subj

        Description:  Test with invalid subject.

        Arguments:

        """

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_attch.return_value = self.fname_list

        self.assertFalse(
            mail_2_rmq.process_file(self.cfg, mock_log, self.subj, self.msg))

    @mock.patch("mail_2_rmq.connect_process", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.process_attach")
    @mock.patch("mail_2_rmq.gen_libs.rm_file")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_invalid_subj_file_err(self, mock_rmq, mock_log, mock_rm,
                                   mock_attch):

        """Function:  test_invalid_subj_file_err

        Description:  Test with invalid subject and with file, but with file
            removal error.

        Arguments:

        """

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_rm.return_value = (True, "Error Message")
        mock_attch.return_value = self.fname_list

        self.assertFalse(
            mail_2_rmq.process_file(self.cfg, mock_log, self.subj2, self.msg))

    @mock.patch("mail_2_rmq.connect_process", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.process_attach")
    @mock.patch("mail_2_rmq.gen_libs.rm_file")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_invalid_subj_file(self, mock_rmq, mock_log, mock_rm, mock_attch):

        """Function:  test_invalid_subj_file

        Description:  Test with invalid subject and with file.

        Arguments:

        """

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_rm.return_value = (False, None)
        mock_attch.return_value = self.fname_list

        self.assertFalse(
            mail_2_rmq.process_file(self.cfg, mock_log, self.subj2, self.msg))

    @mock.patch("mail_2_rmq.connect_process", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.process_attach")
    @mock.patch("mail_2_rmq.gen_libs.rm_file")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_valid_subj_file_err(self, mock_rmq, mock_log, mock_rm,
                                 mock_attch):

        """Function:  test_valid_subj_file_err

        Description:  Test email with valid subj and file, but file remove
            error.

        Arguments:

        """

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_rm.return_value = (True, "Error Message")
        mock_attch.return_value = self.fname_list

        self.assertFalse(
            mail_2_rmq.process_file(self.cfg, mock_log, self.subj, self.msg))

    @mock.patch("mail_2_rmq.connect_process", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.process_attach")
    @mock.patch("mail_2_rmq.gen_libs.rm_file")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.rabbitmq_class.create_rmqpub")
    def test_valid_subj(self, mock_rmq, mock_log, mock_rm, mock_attch):

        """Function:  test_valid_subj

        Description:  Test email with valid subj and file.

        Arguments:

        """

        mock_rmq.return_value = self.rmq
        mock_log.return_value = True
        mock_rm.return_value = (False, None)
        mock_attch.return_value = self.fname_list

        self.assertFalse(
            mail_2_rmq.process_file(self.cfg, mock_log, self.subj, self.msg))


if __name__ == "__main__":
    unittest.main()
