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
        test_empty_msg -> Test empty message is returned.
        test_single_part_msg -> Test single part message is returned.
        test_two_part_msg -> Test two part message is returned.
        test_multi_part_msg -> Test multi-part message is returned.
        test_empty_payload_msg -> Test when payload returns empty.
        test_multipart_empty_payload_msg -> Test multipart & empty payload msg.
        test_multiple_part_msg -> Test returning multiple part messages.

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
                walk -> Stub holder for walk method.

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

        class PartMsgTest(object):

            """Class:  PartMsgTest

            Description:  Is a representation of a part of an email message
                instance.

            Super-Class:  object

            Sub-Classes:  None

            Methods:
                __init__ -> Initialize configuration environment.
                get_content_maintype -> Stub holder for get_content_maintype.
                get_payload -> Stub holder for get_payload method.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the RQTest class.

                Arguments:
                        None

                """

                self.type = ""
                self.payload = ""

            def get_content_maintype(self):

                """Method:  get_content_maintype

                Description:  Stub holder for get_content_maintype method.

                Arguments:
                        None

                """

                return self.type

            def get_payload(self, decode):

                """Method:  get_payload

                Description:  Stub holder for get_payload method.

                Arguments:
                        decode = Place holder for decode variable.

                """

                return self.payload

        self.MSG = MsgTest()
        self.PART_MSG = PartMsgTest()
        self.PART_MSG2 = PartMsgTest()
        self.PART_MSG3 = PartMsgTest()
        self.PART_MSG4 = PartMsgTest()

    def test_multiple_part_msg(self):

        """Function:  test_multiple_part_msg

        Description:  Test returning multiple part messages.

        Arguments:
            None

        """

        self.MSG.walk_list = [self.PART_MSG, self.PART_MSG2, self.PART_MSG3,
                              self.PART_MSG4]
        self.PART_MSG.type = "multipart"
        self.PART_MSG2.type = "single"
        self.PART_MSG2.payload = "Email"
        self.PART_MSG3.type = "single"
        self.PART_MSG3.payload = ""
        self.PART_MSG4.type = "single"
        self.PART_MSG4.payload = " Message"

        self.assertEqual(mail_2_rmq.get_text(self.MSG), "Email Message")

    def test_multipart_empty_payload_msg(self):

        """Function:  test_multipart_empty_payload_msg

        Description:  Test multipart and empty payload msg.

        Arguments:
            None

        """

        self.MSG.walk_list = [self.PART_MSG, self.PART_MSG2, self.PART_MSG3]
        self.PART_MSG.type = "multipart"
        self.PART_MSG2.type = "single"
        self.PART_MSG2.payload = ""
        self.PART_MSG3.type = "single"
        self.PART_MSG3.payload = "Email"

        self.assertEqual(mail_2_rmq.get_text(self.MSG), "Email")

    def test_empty_payload_msg(self):

        """Function:  test_empty_payload_msg

        Description:  Test when payload returns empty.

        Arguments:
            None

        """

        self.MSG.walk_list = [self.PART_MSG, self.PART_MSG2]
        self.PART_MSG.type = "single"
        self.PART_MSG.payload = ""
        self.PART_MSG2.type = "single"
        self.PART_MSG2.payload = "Email"

        self.assertEqual(mail_2_rmq.get_text(self.MSG), "Email")

    def test_multi_part_msg(self):

        """Function:  test_multi_part_msg

        Description:  Test multi-part message is returned.

        Arguments:
            None

        """

        self.MSG.walk_list = [self.PART_MSG, self.PART_MSG2]
        self.PART_MSG.type = "multipart"
        self.PART_MSG2.type = "single"
        self.PART_MSG2.payload = "Email"

        self.assertEqual(mail_2_rmq.get_text(self.MSG), "Email")

    def test_two_part_msg(self):

        """Function:  test_two_part_msg

        Description:  Test two part message is returned.

        Arguments:
            None

        """

        self.MSG.walk_list = [self.PART_MSG, self.PART_MSG]
        self.PART_MSG.type = "single"
        self.PART_MSG.payload = "Email"

        self.assertEqual(mail_2_rmq.get_text(self.MSG), "EmailEmail")

    def test_single_part_msg(self):

        """Function:  test_single_part_msg

        Description:  Test single part message is returned.

        Arguments:
            None

        """

        self.MSG.walk_list = [self.PART_MSG]
        self.PART_MSG.type = "single"
        self.PART_MSG.payload = "Email Message"

        self.assertEqual(mail_2_rmq.get_text(self.MSG), "Email Message")

    def test_empty_msg(self):

        """Function:  test_empty_msg

        Description:  Test empty message is returned.

        Arguments:
            None

        """

        self.assertEqual(mail_2_rmq.get_text(self.MSG), "")


if __name__ == "__main__":
    unittest.main()
