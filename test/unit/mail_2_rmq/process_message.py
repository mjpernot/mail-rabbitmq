#!/usr/bin/python
# Classification (U)

"""Program:  process_message.py

    Description:  Unit testing of process_message in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/process_message.py

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
        test_process_message -> Test parsing an email.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:
            None

        """

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
                self.valid_queues ["QUEUE1", "QUEUE2"]

        self.cfg = CfgTest()

    @mock.patch("mail_2_rmq.connect_process")
    @mock.patch("mail_2_rmq.parse_email")
    @mock.patch("mail_2_rmq.rabbitmq_class.RabbitMQPub")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_process_message(self, mock_log, mock_rmq, mock_parse, mock_conn):

        """Function:  test_process_message

        Description:  Test process an email.

        Arguments:
            mock_log -> Mock Ref:  mail_2_rmq.gen_class.Logger
            mock_rmq -> Mock Ref:  mail_2_rmq.rabbitmq_class.RabbitMQPub
            mock_parse -> Mock Ref:  mail_2_rmq.parse_email
            mock_conn -> Mock Ref:  mail_2_rmq.connect_process

        """

        mock_log.return_value = True
        mock_rmq.return_value = "RabbitMQ Instance"
        mock_parse.return_value = "Email Message"
        mock_conn.return_value = True

        self.assertFalse(mail_2_rmq.process_message())


if __name__ == "__main__":
    unittest.main()
