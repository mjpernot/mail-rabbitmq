# Classification (U)

"""Program:  archive_email.py

    Description:  Unit testing of archive_email in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/archive_email.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import mail_2_rmq                               # pylint:disable=E0401,C0413
import version                                  # pylint:disable=C0413,E0401

__version__ = version.__version__


class RQTest():                                         # pylint:disable=R0903

    """Class:  RQTest

    Description:  Class which is a representation of a RQ class.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the RQTest class.

        Arguments:

        """

        self.exchange = "Test_Exchange"
        self.queue_name = "Test_Queue"

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

        self.email_dir = "/dir/path"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_archive_email

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()
        self.rmq = RQTest()
        self.msg = "Email Message"
        self.dtg = "20190205-124217"

    @mock.patch("mail_2_rmq.gen_libs.write_file")
    @mock.patch("mail_2_rmq.datetime.datetime")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_archive_email(self, mock_log, mock_date, mock_file):

        """Function:  test_archive_email

        Description:  Test archiving an email.

        Arguments:

        """

        mock_log.return_value = True
        mock_date.now.return_value = "(2019, 2, 5, 12, 40, 50, 852147)"
        mock_date.strftime.return_value = self.dtg
        mock_file.return_value = True

        self.assertFalse(
            mail_2_rmq.archive_email(self.rmq, mock_log, self.cfg, self.msg))


if __name__ == "__main__":
    unittest.main()
