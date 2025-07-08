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
import unittest

# Local
sys.path.append(os.getcwd())
import mail_2_rmq                               # pylint:disable=E0401,C0413
import version                                  # pylint:disable=C0413,E0401

__version__ = version.__version__


class MsgTest():

    """Class:  MsgTest

    Description:  Is a representation of a email message instance.

    Methods:
        __init__
        walk
        get_content_type

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the RQTest class.

        Arguments:

        """

        self.walk_list = []
        self.content_type = "text/plain"

    def walk(self):

        """Method:  walk

        Description:  Stub holder for walk method.

        Arguments:

        """

        return self.walk_list

    def get_content_type(self):

        """Method:  get_content_type

        Description:  What is content type of this part of message.

        Arguments:

        """

        return self.content_type


class PartMsgTest2():

    """Class:  PartMsgTest2

    Description:  Is a byte representation of a part of an email message
        instance.

    Methods:
        __init__
        get_content_maintype
        get_payload
        get_content_type

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the RQTest class.

        Arguments:

        """

        self.type = ""
        self.payload = b"Email Message"
        self.decode = None
        self.content_type = "text/plain"

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
            (input) decode

        """

        self.decode = decode

        return self.payload

    def get_content_type(self):

        """Method:  get_content_type

        Description:  What is content type of this part of message.

        Arguments:

        """

        return self.content_type


class PartMsgTest():

    """Class:  PartMsgTest

    Description:  Is a representation of a part of an email message
        instance.

    Methods:
        __init__
        get_content_maintype
        get_payload
        get_content_type

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the RQTest class.

        Arguments:

        """

        self.type = ""
        self.payload = ""
        self.decode = None
        self.content_type = "text/plain"

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
            (input) decode

        """

        self.decode = decode

        return self.payload

    def get_content_type(self):

        """Method:  get_content_type

        Description:  What is content type of this part of message.

        Arguments:

        """

        return self.content_type


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_multiple_part_msg
        test_multipart_empty_payload_msg
        test_empty_payload_msg
        test_multi_part_msg
        test_two_part_msg
        test_single_part_msg_byte
        test_single_part_msg
        test_empty_msg

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.msg = MsgTest()
        self.part_msg = PartMsgTest()
        self.part_msga = PartMsgTest2()
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

    def test_single_part_msg_byte(self):

        """Function:  test_single_part_msg_byte

        Description:  Test single part byte message is returned.

        Arguments:

        """

        self.msg.walk_list = [self.part_msga]
        self.part_msg.type = "single"
        self.part_msg.payload = self.email_msg

        self.assertEqual(mail_2_rmq.get_text(self.msg), self.email_msg)

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
