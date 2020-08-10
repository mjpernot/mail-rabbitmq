#!/usr/bin/python
# Classification (U)

"""Program:  get_text.py

    Description:  Unit testing of get_text in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/get_text.py

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

        """

        class MsgTest(object):

            """Class:  MsgTest

            Description:  Is a representation of a email message instance.

            Methods:
                __init__ -> Initialize configuration environment.
                walk -> Stub holder for walk method.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the RQTest class.

                Arguments:

                """

                self.walk_list = []

            def walk(self):

                """Method:  walk

                Description:  Stub holder for walk method.

                Arguments:

                """

                return self.walk_list

        class PartMsgTest(object):

            """Class:  PartMsgTest

            Description:  Is a representation of a part of an email message
                instance.

            Methods:
                __init__ -> Initialize configuration environment.
                get_content_maintype -> Stub holder for get_content_maintype.
                get_payload -> Stub holder for get_payload method.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the RQTest class.

                Arguments:

                """

                self.type = ""
                self.payload = ""
                self.decode = None

            def get_content_maintype(self):

                """Method:  get_content_maintype

                Description:  Stub holder for get_content_maintype method.

                Arguments:

                """

                return self.type

            def get_payload(self, decode):

                """Method:  get_payload

                Description:  Stub holder for get_payload method.

                Arguments:
                    (input) decode ->  Place holder for decode variable.

                """

                self.decode = decode

                return self.payload

        self.msg = MsgTest()
        self.part_msg = PartMsgTest()
        self.part_msg2 = PartMsgTest()
        self.part_msg3 = PartMsgTest()
        self.part_msg4 = PartMsgTest()
        self.email_msg = "Email Message"

    def test_multiple_part_msg(self):

        """Function:  test_multiple_part_msg

        Description:  Test returning multiple part messages.

        Arguments:

        """

        self.msg.walk_list = [self.part_msg, self.part_msg2, self.part_msg3,
                              self.part_msg4]
        self.part_msg.type = "multipart"
        self.part_msg2.type = "single"
        self.part_msg2.payload = "Email"
        self.part_msg3.type = "single"
        self.part_msg3.payload = ""
        self.part_msg4.type = "single"
        self.part_msg4.payload = " Message"

        self.assertEqual(mail_2_rmq.get_text(self.msg), self.email_msg)

    def test_multipart_empty_payload_msg(self):

        """Function:  test_multipart_empty_payload_msg

        Description:  Test multipart and empty payload msg.

        Arguments:

        """

        self.msg.walk_list = [self.part_msg, self.part_msg2, self.part_msg3]
        self.part_msg.type = "multipart"
        self.part_msg2.type = "single"
        self.part_msg2.payload = ""
        self.part_msg3.type = "single"
        self.part_msg3.payload = "Email"

        self.assertEqual(mail_2_rmq.get_text(self.msg), "Email")

    def test_empty_payload_msg(self):

        """Function:  test_empty_payload_msg

        Description:  Test when payload returns empty.

        Arguments:

        """

        self.msg.walk_list = [self.part_msg, self.part_msg2]
        self.part_msg.type = "single"
        self.part_msg.payload = ""
        self.part_msg2.type = "single"
        self.part_msg2.payload = "Email"

        self.assertEqual(mail_2_rmq.get_text(self.msg), "Email")

    def test_multi_part_msg(self):

        """Function:  test_multi_part_msg

        Description:  Test multi-part message is returned.

        Arguments:

        """

        self.msg.walk_list = [self.part_msg, self.part_msg2]
        self.part_msg.type = "multipart"
        self.part_msg2.type = "single"
        self.part_msg2.payload = "Email"

        self.assertEqual(mail_2_rmq.get_text(self.msg), "Email")

    def test_two_part_msg(self):

        """Function:  test_two_part_msg

        Description:  Test two part message is returned.

        Arguments:

        """

        self.msg.walk_list = [self.part_msg, self.part_msg]
        self.part_msg.type = "single"
        self.part_msg.payload = "Email"

        self.assertEqual(mail_2_rmq.get_text(self.msg), "EmailEmail")

    def test_single_part_msg(self):

        """Function:  test_single_part_msg

        Description:  Test single part message is returned.

        Arguments:

        """

        self.msg.walk_list = [self.part_msg]
        self.part_msg.type = "single"
        self.part_msg.payload = self.email_msg

        self.assertEqual(mail_2_rmq.get_text(self.msg), self.email_msg)

    def test_empty_msg(self):

        """Function:  test_empty_msg

        Description:  Test empty message is returned.

        Arguments:

        """

        self.assertEqual(mail_2_rmq.get_text(self.msg), "")


if __name__ == "__main__":
    unittest.main()
