# Classification (U)

"""Program:  filter_subject.py

    Description:  Unit testing of filter_subject in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/filter_subject.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest

# Local
sys.path.append(os.getcwd())
import mail_2_rmq                               # pylint:disable=E0401,C0413
import version                                  # pylint:disable=C0413,E0401

__version__ = version.__version__


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

        self.subj_filter = r"\[.*\]"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_no_filter
        test_filtering
        test_white_space

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()
        self.subj_base = "package-admin"

    def test_no_filter(self):

        """Function:  test_no_filter

        Description:  No filtering required.

        Arguments:

        """

        self.assertEqual(mail_2_rmq.filter_subject(self.subj_base, self.cfg),
                         self.subj_base)

    def test_filtering(self):

        """Function:  test_filtering

        Description:  Filtering required.

        Arguments:

        """

        subj = "[FromSomePlace] package-admin"

        self.assertEqual(mail_2_rmq.filter_subject(subj, self.cfg),
                         self.subj_base)

    def test_white_space(self):

        """Function:  test_white_space

        Description:  Test stripping white space from right.

        Arguments:

        """

        subj = "[FromSomePlace] package-admin "

        self.assertEqual(mail_2_rmq.filter_subject(subj, self.cfg),
                         self.subj_base)


if __name__ == "__main__":
    unittest.main()
