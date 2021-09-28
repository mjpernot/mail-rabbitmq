#!/usr/bin/python
# Classification (U)

"""Program:  create_rq.py

    Description:  Unit testing of create_rq in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/create_rq.py

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


class CfgTest2(object):

    """Class:  CfgTest2

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
        self.valid_queues = ["QUEUE1", "QUEUE2"]
        self.subj_filter = [r"\[.*\]"]
        self.host_list = ["host1:5672", "host2:5671"]
        self.heartbeat = 120


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
        self.valid_queues = ["QUEUE1", "QUEUE2"]
        self.subj_filter = [r"\[.*\]"]


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_heartbeat_host_list
        test_no_heartbeat_host_list
        test_create_instance

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()
        self.cfg2 = CfgTest2()
        self.q_name = "Queue_Name"
        self.r_key = "Routing_Key"

    @mock.patch("mail_2_rmq.rabbitmq_class.RabbitMQPub")
    def test_heartbeat_host_list(self, mock_rmq):

        """Function:  test_heartbeat_host_list

        Description:  Test with host_list or heartbeat in cfg module.

        Arguments:

        """

        mock_rmq.return_value = "RabbitMQ_Instance"

        self.assertEqual(mail_2_rmq.create_rq(self.cfg2, self.q_name,
                                              self.r_key),
                         "RabbitMQ_Instance")

    @mock.patch("mail_2_rmq.rabbitmq_class.RabbitMQPub")
    def test_no_heartbeat_host_list(self, mock_rmq):

        """Function:  test_no_heartbeat_host_list

        Description:  Test with no host_list or heartbeat in cfg module.

        Arguments:

        """

        mock_rmq.return_value = "RabbitMQ_Instance"

        self.assertEqual(mail_2_rmq.create_rq(self.cfg, self.q_name,
                                              self.r_key),
                         "RabbitMQ_Instance")

    @mock.patch("mail_2_rmq.rabbitmq_class.RabbitMQPub")
    def test_create_instance(self, mock_rmq):

        """Function:  test_create_instance

        Description:  Test creating RabbitMQ Instance.

        Arguments:

        """

        mock_rmq.return_value = "RabbitMQ_Instance"

        self.assertEqual(mail_2_rmq.create_rq(self.cfg, self.q_name,
                                              self.r_key),
                         "RabbitMQ_Instance")


if __name__ == "__main__":
    unittest.main()
