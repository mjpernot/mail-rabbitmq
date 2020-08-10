#!/usr/bin/python
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
        test_archive_email -> Test parsing an email.
        tearDown -> Clean up of unit testing.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        class RQTest(object):

            """Class:  RQTest

            Description:  Class which is a representation of a RQ class.

            Methods:
                __init__ -> Initialize configuration environment.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the RQTest class.

                Arguments:

                """

                self.exchange = "Test_Exchange"
                self.queue_name = "Test_Queue"

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

                self.email_dir = "/dir/path"

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

        self.assertFalse(mail_2_rmq.archive_email(self.rmq, mock_log, self.cfg,
                                                  self.msg))


if __name__ == "__main__":
    unittest.main()
