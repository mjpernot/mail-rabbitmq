#!/usr/bin/python
# Classification (U)

"""Program:  process_attach.py

    Description:  Unit testing of process_attach in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/process_attach.py

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


class MultiPart(object):

    """Class:  MultiPart

    Description:  Class which is a representation of a Email multipart class.

    Methods:
        __init__ -> Initialize configuration environment.
        get_content_type -> What is content type of this part of message.
        get_filename -> Name of attachment in message.
        get_payload -> Data string of attachment.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the RQTest class.

        Arguments:

        """

        self.decode = False
        self.content_type = "application/pdf"
        self.filename = "Filename.pdf"
        self.payload = "Data_Goes_Here"

    def get_content_type(self):

        """Method:  get_content_type

        Description:  What is content type of this part of message.

        Arguments:

        """

        return self.content_type

    def get_filename(self):

        """Method:  get_filename

        Description:  Name of attachment in message.

        Arguments:

        """

        return self.filename

    def get_payload(self, decode):

        """Method:  get_payload

        Description:  Data string of attachment.

        Arguments:

        """

        self.decode = decode

        return self.payload


class Email(object):

    """Class:  Email

    Description:  Class which is a representation of a Email class.

    Methods:
        __init__ -> Initialize configuration environment.
        is_multipart -> Is email message multiple parts.
        walk -> Return list of items to check in email multiple parts.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the RQTest class.

        Arguments:

        """

        self.multipart = True
        self.parts = [MultiPart()]

    def is_multipart(self):

        """Method:  is_multipart

        Description:   Is email message multiple parts.

        Arguments:

        """

        return self.multipart

    def walk(self):

        """Method:  walk

        Description:   Return list of items to check in email multiple parts.

        Arguments:

        """

        return self.parts


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
        self.valid_queues = ["Queue1", "Queue2"]
        self.subj_filter = ["\[.*\]"]
        self.tmp_dir = "test/unit/mail_2_rmq/tmp"
        self.attach_types = ["application/pdf"]


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Unit testing initilization.
        test_one_valid_attach -> Test email with valid subject.
        tearDown -> Clean up of unit testing.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()
        self.msg = Email()
        self.results = os.path.join(self.cfg.tmp_dir, "Filename.pdf.encoded")
        self.fname = "Filename.pdf"

    @mock.patch("mail_2_rmq.gen_libs.rm_file")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_remove_fail(self, mock_log, mock_rm):

        """Function:  test_remove_fail

        Description:  Test with file removal failure.

        Arguments:

        """

        mock_log.return_value = True
        mock_rm.return_value = (True, "Error Message")

        fname = mail_2_rmq.process_attach(self.msg, mock_log, self.cfg)

        self.assertEqual(fname, self.results)

    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_one_valid_attach(self, mock_log):

        """Function:  test_one_valid_attach

        Description:  Test with one valid attachment.

        Arguments:

        """

        mock_log.return_value = True

        fname = mail_2_rmq.process_attach(self.msg, mock_log, self.cfg)

        self.assertEqual(fname, self.results)

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:

        """

        if os.path.isfile(self.results):
            os.remove(self.results)

        if os.path.isfile(os.path.join(self.cfg.tmp_dir, self.fname)):
            os.remove(os.path.join(self.cfg.tmp_dir, self.fname))


if __name__ == "__main__":
    unittest.main()
