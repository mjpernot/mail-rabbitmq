#!/usr/bin/python
# Classification (U)

"""Program:  process_message.py

    Description:  Unit testing of process_message in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/process_message.py

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
        self.queue_dict = {"goodname@domain": "AddrQueue",
                           "goodname2@domain": "AddrQueue2"}


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_missing_from
        test_from_addr
        test_fname_valid_subj
        test_fname_invalid_subj
        test_fname_miss
        test_invalid_subj
        test_valid_subj

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()
        self.email_msg = {"subject": "Queue1", "from": "From: name@domain"}
        self.email_msg2 = {"subject": "invalid", "from": "From: name2@domain"}
        self.email_msg3 = {"subject": "FileQueue1",
                           "from": "From: name3@domain"}
        self.email_msg4 = {"subject": "invalid",
                           "from": "From: goodname@domain"}
        self.email_list = ["name@domain"]
        self.email_list2 = ["goodname@domain"]

    @mock.patch("mail_2_rmq.process_file", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.get_email_addr")
    @mock.patch("mail_2_rmq.camelize")
    @mock.patch("mail_2_rmq.filter_subject")
    @mock.patch("mail_2_rmq.parse_email")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_missing_from(self, mock_log, mock_parse, mock_filter, mock_camel,
                          mock_email):

        """Function:  test_missing_from

        Description:  Test with missing from line from email.

        Arguments:

        """

        mock_email.return_value = list()
        mock_log.return_value = True
        mock_parse.return_value = self.email_msg4
        mock_filter.return_value = "InvalidQueue"
        mock_camel.return_value = "InvalidQueue"

        self.assertFalse(mail_2_rmq.process_message(self.cfg, mock_log))

    @mock.patch("mail_2_rmq.process_from", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.get_email_addr")
    @mock.patch("mail_2_rmq.camelize")
    @mock.patch("mail_2_rmq.filter_subject")
    @mock.patch("mail_2_rmq.parse_email")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_from_addr(self, mock_log, mock_parse, mock_filter, mock_camel,
                       mock_email):

        """Function:  test_from_addr

        Description:  Test with file attachment found and valid subject.

        Arguments:

        """

        mock_email.return_value = self.email_list2
        mock_log.return_value = True
        mock_parse.return_value = self.email_msg4
        mock_filter.return_value = "InvalidQueue"
        mock_camel.return_value = "InvalidQueue"

        self.assertFalse(mail_2_rmq.process_message(self.cfg, mock_log))

    @mock.patch("mail_2_rmq.process_file", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.get_email_addr")
    @mock.patch("mail_2_rmq.camelize")
    @mock.patch("mail_2_rmq.filter_subject")
    @mock.patch("mail_2_rmq.parse_email")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_fname_valid_subj(self, mock_log, mock_parse, mock_filter,
                              mock_camel, mock_email):

        """Function:  test_fname_valid_subj

        Description:  Test with file attachment found and valid subject.

        Arguments:

        """

        mock_email.return_value = self.email_list
        mock_log.return_value = True
        mock_parse.return_value = self.email_msg3
        mock_filter.return_value = "FileQueue1"
        mock_camel.return_value = "FileQueue1"

        self.assertFalse(mail_2_rmq.process_message(self.cfg, mock_log))

    @mock.patch("mail_2_rmq.process_file", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.get_email_addr")
    @mock.patch("mail_2_rmq.camelize")
    @mock.patch("mail_2_rmq.filter_subject")
    @mock.patch("mail_2_rmq.parse_email")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_fname_invalid_subj(self, mock_log, mock_parse, mock_filter,
                                mock_camel, mock_email):

        """Function:  test_fname_invalid_subj

        Description:  Test with file attachment found, but invalid subject.

        Arguments:

        """

        mock_email.return_value = self.email_list
        mock_log.return_value = True
        mock_parse.return_value = self.email_msg2
        mock_filter.return_value = "invalid"
        mock_camel.return_value = "Invalid"

        self.assertFalse(mail_2_rmq.process_message(self.cfg, mock_log))

    @mock.patch("mail_2_rmq.process_file", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.get_email_addr")
    @mock.patch("mail_2_rmq.camelize")
    @mock.patch("mail_2_rmq.filter_subject")
    @mock.patch("mail_2_rmq.parse_email")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_fname_miss(self, mock_log, mock_parse, mock_filter, mock_camel,
                        mock_email):

        """Function:  test_fname_miss

        Description:  Test with file name missing, no attachment found.

        Arguments:

        """

        mock_email.return_value = self.email_list
        mock_log.return_value = True
        mock_parse.return_value = self.email_msg2
        mock_camel.return_value = "Invalid"
        mock_filter.return_value = "invalid"

        self.assertFalse(mail_2_rmq.process_message(self.cfg, mock_log))

    @mock.patch("mail_2_rmq.process_file", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.get_email_addr")
    @mock.patch("mail_2_rmq.camelize")
    @mock.patch("mail_2_rmq.filter_subject")
    @mock.patch("mail_2_rmq.parse_email")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_invalid_subj(self, mock_log, mock_parse, mock_filter, mock_camel,
                          mock_email):

        """Function:  test_invalid_subj

        Description:  Test email with invalid subject.

        Arguments:

        """

        mock_email.return_value = self.email_list
        mock_log.return_value = True
        mock_parse.return_value = self.email_msg2
        mock_camel.return_value = "Invalid"
        mock_filter.return_value = "invalid"

        self.assertFalse(mail_2_rmq.process_message(self.cfg, mock_log))

    @mock.patch("mail_2_rmq.process_subj", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.get_email_addr")
    @mock.patch("mail_2_rmq.camelize")
    @mock.patch("mail_2_rmq.filter_subject")
    @mock.patch("mail_2_rmq.parse_email")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_valid_subj(self, mock_log, mock_parse, mock_filter, mock_camel,
                        mock_email):

        """Function:  test_valid_subj

        Description:  Test email with valid subject.

        Arguments:

        """

        mock_email.return_value = self.email_list
        mock_log.return_value = True
        mock_parse.return_value = self.email_msg
        mock_filter.return_value = self.email_msg["subject"]
        mock_camel.return_value = self.email_msg["subject"]

        self.assertFalse(mail_2_rmq.process_message(self.cfg, mock_log))


if __name__ == "__main__":
    unittest.main()
