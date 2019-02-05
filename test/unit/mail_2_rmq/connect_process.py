#!/usr/bin/python
# Classification (U)

"""Program:  connect_process.py

    Description:  Unit testing of connect_process in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/connect_process.py

    Arguments:
        None

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
import collections

# Local
sys.path.append(os.getcwd())
import mail_2_rmq
import version

# Version
__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Super-Class:  unittest.TestCase

    Sub-Classes:  None

    Methods:
        setUp -> Unit testing initilization.
        test_true_true_connect -> Test connection with true/true status.
        test_false_false_connect -> Test connection with false/false status.
        test_false_true_connect -> Test connection with false/true status.
        test_true_false_connect -> Test connection with true/false status.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:
            None

        """

        class RQTest(object):

            """Class:  RQTest

            Description:  Class which is a representation of a RQ class.

            Super-Class:  object

            Sub-Classes:  None

            Methods:
                __init__ -> Initialize configuration environment.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the RQTest class.

                Arguments:
                        None

                """

                self.exchange = "Test_Exchange"
                self.queue_name = "Test_Queue"
                self.status = collections.namedtuple("RQ", "is_open")
                self.channel = self.status(True)
                self.conn_status = True
                self.err_msg = ""
                self.pub_status = True

            def create_connection(self):

                """Method:  create_connection

                Description:  Stub holder for create_connection method.

                Arguments:
                        None

                """

                return self.conn_status, self.err_msg

            def publish_msg(self, msg):

                """Method:  publish_msg

                Description:  Stub holder for publish_msg method.

                Arguments:
                        None

                """

                return self.pub_status

            def change_channel(self, stat):

                """Method:  change_channel

                Description:  Change channel status.

                Arguments:
                        None

                """

                self.channel = self.status(stat)

        class CfgTest(object):

            """Class:  CfgTest

            Description:  Class which is a representation of a cfg module.

            Super-Class:  object

            Sub-Classes:  None

            Methods:
                __init__ -> Initialize configuration environment.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the CfgTest class.

                Arguments:
                        None

                """

                self.email_dir = os.path.join(os.getcwd(),
                                              "test/unit/mail_2_rmq/tmp")
                self.host = "HOSTNAME"
                self.exchange_name = "EXCHANGE_NAME"
                self.err_queue = "ERROR_QUEUE"

        self.cfg = CfgTest()
        self.RQ = RQTest()

        #self.msg = {"from": "From_Address",
        #            "to": "To_Address",
        #            "subject": "EmailSubject"}

    #@unittest.skip("Done")
    @mock.patch("mail_2_rmq.email")
    @mock.patch("mail_2_rmq.archive_email")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_true_true_connect(self, mock_log, mock_archive, mock_msg):

        """Function:  test_true_true_connect

        Description:  Test connecting to RabbitMQ with true/true status.

        Arguments:
            mock_log -> Mock Ref:  mail_2_rmq.gen_class.Logger
            mock_archive -> Mock Ref:  mail_2_rmq.archive_email
            mock_msg -> Mock Ref:  mail_2_rmq.email

        """

        mock_log.return_value = True
        mock_archive.return_value = True
        mock_msg.get_payload.return_value = "Email message"

        self.assertFalse(mail_2_rmq.connect_process(self.RQ, mock_log,
                                                    self.cfg, mock_msg))

    @unittest.skip("Done")
    @mock.patch("mail_2_rmq.archive_email")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_false_false_connect(self, mock_log, mock_archive):

        """Function:  test_false_false_connect

        Description:  Test connecting to RabbitMQ with false/false status.

        Arguments:
            mock_log -> Mock Ref:  mail_2_rmq.gen_class.Logger
            mock_archive -> Mock Ref:  mail_2_rmq.archive_email

        """

        mock_log.return_value = True
        mock_archive.return_value = True

        self.RQ.conn_status = False
        self.RQ.change_channel(False)
        self.assertFalse(mail_2_rmq.connect_process(self.RQ, mock_log,
                                                    self.cfg, ""))

    @unittest.skip("Done")
    @mock.patch("mail_2_rmq.archive_email")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_false_true_connect(self, mock_log, mock_archive):

        """Function:  test_false_true_connect

        Description:  Test connecting to RabbitMQ with false/true status.

        Arguments:
            mock_log -> Mock Ref:  mail_2_rmq.gen_class.Logger
            mock_archive -> Mock Ref:  mail_2_rmq.archive_email

        """

        mock_log.return_value = True
        mock_archive.return_value = True

        self.RQ.conn_status = False
        self.assertFalse(mail_2_rmq.connect_process(self.RQ, mock_log,
                                                    self.cfg, ""))

    @unittest.skip("Done")
    @mock.patch("mail_2_rmq.archive_email")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_true_false_connect(self, mock_log, mock_archive):

        """Function:  test_true_false_connect

        Description:  Test connecting to RabbitMQ with true/false status.

        Arguments:
            mock_log -> Mock Ref:  mail_2_rmq.gen_class.Logger
            mock_archive -> Mock Ref:  mail_2_rmq.archive_email

        """

        mock_log.return_value = True
        mock_archive.return_value = True

        self.RQ.change_channel(False)
        self.assertFalse(mail_2_rmq.connect_process(self.RQ, mock_log,
                                                    self.cfg, ""))


if __name__ == "__main__":
    unittest.main()
