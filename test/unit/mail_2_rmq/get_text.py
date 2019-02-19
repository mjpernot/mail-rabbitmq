#!/usr/bin/python
# Classification (U)

"""Program:  get_text.py

    Description:  Unit testing of get_text in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/get_text.py

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

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:
            None

        """

        class MsgTest(object):

            """Class:  MsgTest

            Description:  Is a representation of a email message instance.

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

                self.walk_list = []

            def walk(self):

                """Method:  walk

                Description:  Stub holder for walk method.

                Arguments:
                        None

                """

                return self.walk_list

        self.MSG = MsgTest()

    def test_empty_msg(self):

        """Function:  test_empty_msg

        Description:  Test empty message is returned.

        Arguments:
            None

        """

        self.assertEqual(mail_2_rmq.get_text(self.MSG), "")


if __name__ == "__main__":
    unittest.main()
