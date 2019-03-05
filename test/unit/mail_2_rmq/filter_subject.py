#!/usr/bin/python
# Classification (U)

"""Program:  filter_subject.py

    Description:  Unit testing of filter_subject in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/filter_subject.py

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
        test_no_filter -> No filtering required.
        test_filtering -> Filtering required.
        test_white_space -> Test stripping white space from right.

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

                self.subj_filter = ["\[.*\]"]

        self.cfg = CfgTest()

        self.subj_base = "package-admin"

    def test_no_filter(self):

        """Function:  test_no_filter

        Description:  No filtering required.

        Arguments:
            None

        """

        self.assertEqual(mail_2_rmq.filter_subject(self.subj_base, self.cfg),
                         self.subj_base)

    def test_filtering(self):

        """Function:  test_filtering

        Description:  Filtering required.

        Arguments:
            None

        """

        subj = "[FromSomePlace] package-admin"
        self.assertEqual(mail_2_rmq.filter_subject(subj, self.cfg),
                         self.subj_base)

    def test_white_space(self):

        """Function:  test_white_space

        Description:  Test stripping white space from right.

        Arguments:
            None

        """

        subj = "[FromSomePlace] package-admin "
        self.assertEqual(mail_2_rmq.filter_subject(subj, self.cfg),
                         self.subj_base)


if __name__ == "__main__":
    unittest.main()
