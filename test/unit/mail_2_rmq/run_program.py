# Classification (U)

"""Program:  run_program.py

    Description:  Unit testing of run_program in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/run_program.py

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
import mail_2_rmq
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


def process_message(cfg, log):

    """Function:  process_message

    Description:  This is a function stub for mail_2_rmq.process_message.

    Arguments:
        (input) cfg
        (input) log

    """

    status = True

    if cfg and log:
        status = True

    return status


def check_nonprocess(cfg, log):

    """Function:  check_nonprocess

    Description:  This is a function stub for mail_2_rmq.check_nonprocess.

    Arguments:
        (input) cfg
        (input) log

    """

    status = True

    if cfg and log:
        status = True

    return status


class ArgParser(object):

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        get_args_keys
        get_val

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args = dict()

    def get_args_keys(self):

        """Method:  get_args_keys

        Description:  Method stub holder for gen_class.ArgParser.get_args_keys.

        Arguments:

        """

        return list(self.args_array.keys())

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args.get(skey, def_val)


class LoggerTest(object):

    """Class:  LoggerTest

    Description:  Class which is a representation of a Logger class.

    Methods:
        __init__
        log_info
        log_warn
        log_close

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the LoggerTest class.

        Arguments:

        """

        self.data = None

    def log_info(self, data):

        """Method:  log_info

        Description:  Stub holder for Logger.log_info method.

        Arguments:
            (input) data

        """

        self.data = data

    def log_warn(self, data):

        """Method:  log_warn

        Description:  Stub holder for Logger.log_warn method.

        Arguments:
            (input) data

        """

        self.data = data

    def log_close(self):

        """Method:  log_close

        Description:  Stub holder for Logger.log_close method.

        Arguments:

        """

        pass


class ProgramLock(object):

    """Class:  ProgramLock

    Description:  Class stub holder for gen_class.ProgramLock class.

    Methods:
        __init__

    """

    def __init__(self, cmdline, flavor):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            (input) cmdline
            (input) flavor

        """

        self.cmdline = cmdline
        self.flavor = flavor


class CfgTest(object):

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
        self.attach_types = ["application/pdf"]
        self.file_queues = ["FileQueue1", "FileQueue2"]
        self.err_file_queue = "ERROR_FILE_QUEUE"
        self.log_file = "LOG_FILE"
        self.email_dir = "EMAIL_DIRECTORY"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_flavor_id
        test_exception_handler
        test_all_func
        test_true_func
        test_true_status
        test_false_status

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()
        self.log = LoggerTest()
        self.proglock = ProgramLock(["cmdline"], "FlavorID")
        self.args = ArgParser()
        self.args2 = ArgParser()
        self.args.args_array = {"-c": "CONFIG_FILE", "-d": "CONFIG_DIRECTORY"}
        self.args2.args_array = {
            "-c": "CONFIG_FILE", "-d": "CONFIG_DIRECTORY", "-y": "flavorid"}
        self.func_names = {"-M": process_message, "-C": check_nonprocess}
        self.err_msgs = ["Error Msg1", "Error Msg3"]

    @mock.patch("mail_2_rmq.gen_class")
    @mock.patch("mail_2_rmq.load_cfg")
    def test_flavor_id(self, mock_cfg, mock_class):

        """Function:  test_flavor_id

        Description:  Test with -y option passed.

        Arguments:

        """

        mock_cfg.return_value = (self.cfg, True, [])
        mock_class.Logger.return_value = self.log

        self.assertFalse(mail_2_rmq.run_program(self.args2, self.func_names))

    @mock.patch("mail_2_rmq.gen_class.Logger")
    @mock.patch("mail_2_rmq.gen_class.ProgramLock")
    @mock.patch("mail_2_rmq.load_cfg")
    def test_exception_handler(self, mock_cfg, mock_lock, mock_log):

        """Function:  test_exception_handler

        Description:  Test with exception handler.

        Arguments:

        """

        mock_cfg.return_value = (self.cfg, True, [])
        mock_log.return_value = self.log
        mock_lock.side_effect = mail_2_rmq.gen_class.SingleInstanceException

        self.assertFalse(mail_2_rmq.run_program(self.args, self.func_names))

    @mock.patch("mail_2_rmq.gen_class")
    @mock.patch("mail_2_rmq.load_cfg")
    def test_all_func(self, mock_cfg, mock_class):

        """Function:  test_all_func

        Description:  Test with all functions.

        Arguments:

        """

        mock_cfg.return_value = (self.cfg, True, [])
        mock_class.Logger.return_value = self.log
        mock_class.ProgramLock.return_value = self.proglock

        self.args.args_array["-M"] = True
        self.args.args_array["-C"] = True
        self.assertFalse(mail_2_rmq.run_program(self.args, self.func_names))

    @mock.patch("mail_2_rmq.gen_class")
    @mock.patch("mail_2_rmq.load_cfg")
    def test_true_func(self, mock_cfg, mock_class):

        """Function:  test_true_func

        Description:  Test with true status and function.

        Arguments:

        """

        mock_cfg.return_value = (self.cfg, True, [])
        mock_class.Logger.return_value = self.log
        mock_class.ProgramLock.return_value = self.proglock

        self.args.args_array["-M"] = True
        self.assertFalse(mail_2_rmq.run_program(self.args, self.func_names))

    @mock.patch("mail_2_rmq.gen_class")
    @mock.patch("mail_2_rmq.load_cfg")
    def test_true_status(self, mock_cfg, mock_class):

        """Function:  test_true_status

        Description:  Test with true status flag.

        Arguments:

        """

        mock_cfg.return_value = (self.cfg, True, [])
        mock_class.Logger.return_value = self.log

        self.assertFalse(mail_2_rmq.run_program(self.args, self.func_names))

    @mock.patch("mail_2_rmq.load_cfg")
    def test_false_status(self, mock_cfg):

        """Function:  test_false_status

        Description:  Test with false status flag.

        Arguments:

        """

        mock_cfg.return_value = (self.cfg, False, self.err_msgs)

        with gen_libs.no_std_out():
            self.assertFalse(
                mail_2_rmq.run_program(self.args, self.func_names))


if __name__ == "__main__":
    unittest.main()
