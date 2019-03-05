#!/usr/bin/python
# Classification (U)

"""Program:  archive_email.py

    Description:  Unit testing of archive_email in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/archive_email.py

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
        test_archive_email -> Test parsing an email.
        tearDown -> Clean up of unit testing.

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

        self.cfg = CfgTest()
        self.RQ = RQTest()

        self.msg = "Email Message"
        self.dtg = "20190205-124217"

        self.e_file = self.RQ.exchange + "-" + self.RQ.queue_name + "-" \
            + self.dtg + ".email.txt"
        self.full_e_file = self.cfg.email_dir + os.path.sep + self.e_file

    @mock.patch("mail_2_rmq.gen_libs.write_file")
    @mock.patch("mail_2_rmq.datetime.datetime")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_archive_email(self, mock_log, mock_date, mock_file):

        """Function:  test_archive_email

        Description:  Test archiving an email.

        Arguments:
            mock_log -> Mock Ref:  mail_2_rmq.gen_class.Logger
            mock_date -> Mock Ref:  mail_2_rmq.datetime.datetime
            mock_file -> Mock Ref:  mail_2_rmq.gen_libs.write_file

        """

        mock_log.return_value = True
        mock_date.now.return_value = "(2019, 2, 5, 12, 40, 50, 852147)"
        mock_date.strftime.return_value = self.dtg
        mock_file.return_value = True

        self.assertFalse(mail_2_rmq.archive_email(self.RQ, mock_log, self.cfg,
                                                  self.msg))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:
            None

        """

        pass


if __name__ == "__main__":
    unittest.main()
