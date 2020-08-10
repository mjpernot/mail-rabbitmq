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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Unit testing initilization.
        test_invalid_subj -> Test email with invalid subject.
        test_valid_subj -> Test email with valid subject.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

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
                self.passwd = "PASSWD"
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

        self.cfg = CfgTest()
        self.email_msg = {"subject": "Queue1"}

    @mock.patch("mail_2_rmq.filter_subject")
    @mock.patch("mail_2_rmq.connect_process")
    @mock.patch("mail_2_rmq.parse_email")
    @mock.patch("mail_2_rmq.create_rq")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_invalid_subj(self, mock_log, mock_rq, mock_parse, mock_conn,
                          mock_filter):

        """Function:  test_invalid_subj

        Description:  Test email with invalid subject.

        Arguments:

        """

        mock_log.return_value = True
        mock_rq.return_value = "RabbitMQ Instance"
        mock_parse.return_value = {"subject": "invalid"}
        mock_conn.return_value = True
        mock_filter.return_value = "invalid"

        self.assertFalse(mail_2_rmq.process_message(self.cfg, mock_log))

    @mock.patch("mail_2_rmq.camelize")
    @mock.patch("mail_2_rmq.filter_subject")
    @mock.patch("mail_2_rmq.connect_process")
    @mock.patch("mail_2_rmq.parse_email")
    @mock.patch("mail_2_rmq.create_rq")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_valid_subj(self, mock_log, mock_rq, mock_parse, mock_conn,
                        mock_filter, mock_camel):

        """Function:  test_valid_subj

        Description:  Test email with valid subject.

        Arguments:

        """

        mock_log.return_value = True
        mock_rq.return_value = "RabbitMQ Instance"
        mock_parse.return_value = self.email_msg
        mock_conn.return_value = True
        mock_filter.return_value = self.email_msg["subject"]
        mock_camel.return_value = self.email_msg["subject"]

        self.assertFalse(mail_2_rmq.process_message(self.cfg, mock_log))


if __name__ == "__main__":
    unittest.main()
