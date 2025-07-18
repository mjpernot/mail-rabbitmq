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
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import mail_2_rmq                               # pylint:disable=E0401,C0413
import version                                  # pylint:disable=C0413,E0401

__version__ = version.__version__


class MultiPart():

    """Class:  MultiPart

    Description:  Class which is a representation of a Email multipart class.

    Methods:
        __init__
        get_content_type
        get_filename
        get_payload

    """

    def __init__(self, content_type, filename):

        """Method:  __init__

        Description:  Initialization instance of the RQTest class.

        Arguments:
            (input) content_type -> Type of attachment.
            (input) filename -> Name of attachment.

        """

        self.decode = False
        self.content_type = content_type
        self.filename = filename
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

    def get_payload(self, decode=False):

        """Method:  get_payload

        Description:  Data string of attachment.

        Arguments:

        """

        self.decode = decode

        return self.payload


class Email():

    """Class:  Email

    Description:  Class which is a representation of a Email class.

    Methods:
        __init__
        is_multipart
        walk

    """

    def __init__(self, content_type, filename):

        """Method:  __init__

        Description:  Initialization instance of the RQTest class.

        Arguments:
            (input) content_type -> Type of attachment.
            (input) filename -> Name of attachment.

        """

        self.multipart = True
        self.parts = [MultiPart(content_type, filename)]

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


class Email2():

    """Class:  Email2

    Description:  Class which is a representation of a Email class.

    Methods:
        __init__
        is_multipart
        walk

    """

    def __init__(self, content_type, filename, content_type2, filename2):

        """Method:  __init__

        Description:  Initialization instance of the RQTest class.

        Arguments:
            (input) content_type -> Type of attachment.
            (input) filename -> Name of attachment.

        """

        self.multipart = True
        self.parts = [MultiPart(content_type, filename),
                      MultiPart(content_type2, filename2)]

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
        self.subj_filter = [r"\[.*\]"]
        self.tmp_dir = "test/unit/mail_2_rmq/tmp"
        self.attach_types = ["application/pdf", "text/plain"]


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_multiple_attach_multiple_types
        test_multiple_attach_no_invalid
        test_multiple_attach_one_invalid
        test_multiple_valid_attach
        test_remove_fail
        test_one_valid_attach
        tearDown

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.fname_encode = "Filename.pdf.encoded"
        self.fname_encode2 = "Filename.txt.encoded"
        self.app_pdf = "application/pdf"
        self.app_zip = "application/zip"
        self.text_plain = "text/plain"
        self.cfg = CfgTest()
        self.results = [os.path.join(self.cfg.tmp_dir, self.fname_encode)]
        self.results2 = [
            os.path.join(self.cfg.tmp_dir, self.fname_encode),
            os.path.join(self.cfg.tmp_dir, "Filename2.pdf.encoded")]
        self.results3 = [
            os.path.join(self.cfg.tmp_dir, self.fname_encode),
            os.path.join(self.cfg.tmp_dir, "Filename.zip.encoded")]
        self.results4 = [os.path.join(self.cfg.tmp_dir, self.fname_encode2)]
        self.fname = "Filename.pdf"
        self.fname2 = "Filename2.pdf"
        self.fname3 = "Filename.zip"
        self.fname4 = "Filename.zip"
        self.fname5 = "Filename.txt"

    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_valid_text_attach(self, mock_log):

        """Function:  test_valid_text_attach

        Description:  Test with valid text attachment.

        Arguments:

        """

        mock_log.return_value = True

        msg = Email(content_type=self.text_plain, filename=self.fname5)

        fname = mail_2_rmq.process_attach(msg, mock_log, self.cfg)

        self.assertEqual(fname, self.results4)

    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_multiple_attach_multiple_types(self, mock_log):

        """Function:  test_multiple_attach_multiple_types

        Description:  Test with multiple attachments with multiple valid types.

        Arguments:

        """

        mock_log.return_value = True

        msg = Email2(
            content_type=self.app_pdf, filename=self.fname,
            content_type2=self.app_zip, filename2=self.fname3)
        self.cfg.attach_types = [self.app_pdf, self.app_zip]

        fname = mail_2_rmq.process_attach(msg, mock_log, self.cfg)

        self.assertEqual(fname, self.results3)

    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_multiple_attach_no_invalid(self, mock_log):

        """Function:  test_multiple_attach_no_invalid

        Description:  Test with multiple attachments with no invalid
            attachments.

        Arguments:

        """

        mock_log.return_value = True

        msg = Email2(
            content_type=self.app_zip, filename=self.fname3,
            content_type2=self.app_zip, filename2=self.fname4)

        fname = mail_2_rmq.process_attach(msg, mock_log, self.cfg)

        self.assertEqual(fname, [])

    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_multiple_attach_one_invalid(self, mock_log):

        """Function:  test_multiple_attach_one_invalid

        Description:  Test with multiple attachments with invalid attachment.

        Arguments:

        """

        mock_log.return_value = True

        msg = Email2(
            content_type=self.app_pdf, filename=self.fname,
            content_type2=self.app_zip, filename2=self.fname3)

        fname = mail_2_rmq.process_attach(msg, mock_log, self.cfg)

        self.assertEqual(fname, self.results)

    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_multiple_valid_attach(self, mock_log):

        """Function:  test_multiple_valid_attach

        Description:  Test with multiple valid attachments.

        Arguments:

        """

        mock_log.return_value = True

        msg = Email2(
            content_type=self.app_pdf, filename=self.fname,
            content_type2=self.app_pdf, filename2=self.fname2)

        fname = mail_2_rmq.process_attach(msg, mock_log, self.cfg)

        self.assertEqual(fname, self.results2)

    @mock.patch("mail_2_rmq.gen_libs.rm_file")
    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_remove_fail(self, mock_log, mock_rm):

        """Function:  test_remove_fail

        Description:  Test with file removal failure.

        Arguments:

        """

        mock_log.return_value = True
        mock_rm.return_value = (True, "Error Message")

        msg = Email(content_type=self.app_pdf, filename=self.fname)

        fname = mail_2_rmq.process_attach(msg, mock_log, self.cfg)

        self.assertEqual(fname, self.results)

    @mock.patch("mail_2_rmq.gen_class.Logger")
    def test_one_valid_attach(self, mock_log):

        """Function:  test_one_valid_attach

        Description:  Test with one valid attachment.

        Arguments:

        """

        mock_log.return_value = True

        msg = Email(content_type=self.app_pdf, filename=self.fname)

        fname = mail_2_rmq.process_attach(msg, mock_log, self.cfg)

        self.assertEqual(fname, self.results)

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:

        """

        for item in self.results:
            if os.path.isfile(item):
                os.remove(item)

        for item in self.results2:
            if os.path.isfile(item):
                os.remove(item)

        for item in self.results3:
            if os.path.isfile(item):
                os.remove(item)

        for item in self.results4:
            if os.path.isfile(item):
                os.remove(item)

        if os.path.isfile(os.path.join(self.cfg.tmp_dir, self.fname)):
            os.remove(os.path.join(self.cfg.tmp_dir, self.fname))

        if os.path.isfile(os.path.join(self.cfg.tmp_dir, self.fname2)):
            os.remove(os.path.join(self.cfg.tmp_dir, self.fname2))

        if os.path.isfile(os.path.join(self.cfg.tmp_dir, self.fname3)):
            os.remove(os.path.join(self.cfg.tmp_dir, self.fname3))

        if os.path.isfile(os.path.join(self.cfg.tmp_dir, self.fname5)):
            os.remove(os.path.join(self.cfg.tmp_dir, self.fname5))


if __name__ == "__main__":
    unittest.main()
