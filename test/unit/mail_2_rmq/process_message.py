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
        __init__ -> Initialize configuration environment.

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
        self.subj_filter = ["\[.*\]"]
        self.tmp_dir = "test/unit/mail_2_rmq/tmp"
        self.attach_types = ["application/pdf"]
        self.file_queue = "FileQueue"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Unit testing initilization.
        test_fname_error -> Test with error removing file.
        test_fname_valid -> Test with attachment found.
        test_fname_invalid -> Test with no attachment found.
        test_invalid_subj -> Test email with invalid subject.
        test_valid_subj -> Test email with valid subject.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()
        self.email_msg = {"subject": "Queue1"}

    @mock.patch("mail_2_rmq.process_attach", mock.Mock(return_value="Fname"))
    @mock.patch("mail_2_rmq.connect_process", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.create_rq", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.gen_libs.rm_file")
    @mock.patch("mail_2_rmq.filter_subject")
    @mock.patch("mail_2_rmq.parse_email")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_fname_error(self, mock_log, mock_parse, mock_filter, mock_rm):

        """Function:  test_fname_error

        Description:  Test with error removing file.

        Arguments:

        """

        mock_log.return_value = True
        mock_parse.return_value = {"subject": "invalid"}
        mock_filter.return_value = "invalid"
        mock_rm.return_value = (True, "Error Message")

        self.assertFalse(mail_2_rmq.process_message(self.cfg, mock_log))

    @mock.patch("mail_2_rmq.process_attach", mock.Mock(return_value="Fname"))
    @mock.patch("mail_2_rmq.connect_process", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.create_rq", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.gen_libs.rm_file")
    @mock.patch("mail_2_rmq.filter_subject")
    @mock.patch("mail_2_rmq.parse_email")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_fname_valid(self, mock_log, mock_parse, mock_filter, mock_rm):

        """Function:  test_fname_valid

        Description:  Test with attachment found.

        Arguments:

        """

        mock_log.return_value = True
        mock_parse.return_value = {"subject": "invalid"}
        mock_filter.return_value = "invalid"
        mock_rm.return_value = (False, None)

        self.assertFalse(mail_2_rmq.process_message(self.cfg, mock_log))

    @mock.patch("mail_2_rmq.process_attach", mock.Mock(return_value=None))
    @mock.patch("mail_2_rmq.connect_process", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.create_rq", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.filter_subject")
    @mock.patch("mail_2_rmq.parse_email")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_fname_invalid(self, mock_log, mock_parse, mock_filter):

        """Function:  test_fname_invalid

        Description:  Test with no attachment found.

        Arguments:

        """

        mock_log.return_value = True
        mock_parse.return_value = {"subject": "invalid"}
        mock_filter.return_value = "invalid"

        self.assertFalse(mail_2_rmq.process_message(self.cfg, mock_log))

    @mock.patch("mail_2_rmq.process_attach", mock.Mock(return_value=None))
    @mock.patch("mail_2_rmq.connect_process", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.create_rq", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.filter_subject")
    @mock.patch("mail_2_rmq.parse_email")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_invalid_subj(self, mock_log, mock_parse, mock_filter):

        """Function:  test_invalid_subj

        Description:  Test email with invalid subject.

        Arguments:

        """

        mock_log.return_value = True
        mock_parse.return_value = {"subject": "invalid"}
        mock_filter.return_value = "invalid"

        self.assertFalse(mail_2_rmq.process_message(self.cfg, mock_log))

    @mock.patch("mail_2_rmq.connect_process", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.create_rq", mock.Mock(return_value=True))
    @mock.patch("mail_2_rmq.camelize")
    @mock.patch("mail_2_rmq.filter_subject")
    @mock.patch("mail_2_rmq.parse_email")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_valid_subj(self, mock_log, mock_parse, mock_filter, mock_camel):

        """Function:  test_valid_subj

        Description:  Test email with valid subject.

        Arguments:

        """

        mock_log.return_value = True
        mock_parse.return_value = self.email_msg
        mock_filter.return_value = self.email_msg["subject"]
        mock_camel.return_value = self.email_msg["subject"]

        self.assertFalse(mail_2_rmq.process_message(self.cfg, mock_log))


if __name__ == "__main__":
    unittest.main()
