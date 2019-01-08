#!/usr/bin/python
# Classification (U)

"""Program:  test_process_message.py

    Description:  Unit testing of process_message in mail_2_rmq.py.

    Usage:
        cat test/unit/mail_2_rmq/test_mail.txt |\
            test/unit/mail_2_rmq/test_process_message.py -G

        cat test/unit/mail_2_rmq/test_mail2.txt |\
            test/unit/mail_2_rmq/test_process_message.py -B

    Arguments:
        None

"""

# Libraries and Global Variables

# Standard
import sys
import os
import re

# Third-party

# Local
sys.path.append(os.getcwd())
import mail_2_rmq
import lib.arg_parser as arg_parser
import lib.gen_class as gen_class
import version

# Version
__version__ = version.__version__


def test_process_message(cfg_name, cfg_dir, pattern):

    """Function:  test_process_message

    Description:  Test mail_2_rmq.process_message function.

    Arguments:
        (input) cfg_name -> Configuration file name.
        (input) cfg_dir -> Directory path to the configuration file.
        (input) pattern -> Search pattern to determine if message is valid.

    """

    pattern1 = pattern
    pattern2 = "INFO Message ingested into RabbitMQ"
    msg_stat1 = False
    msg_stat2 = False
    hold = []

    cfg, status_flag = mail_2_rmq.load_cfg(cfg_name, cfg_dir)

    if status_flag:

        if os.path.isfile(cfg.log_file):
            os.remove(cfg.log_file)

        LOG = gen_class.Logger(cfg.log_file, cfg.log_file, "INFO",
                               "%(asctime)s %(levelname)s %(message)s",
                               "%Y-%m-%dT%H:%M:%SZ")

        mail_2_rmq.process_message(cfg, LOG)

        LOG.log_close()

        f_hdlr = open(cfg.log_file, "r")

        for line in f_hdlr:
            hold.append(line)

            if re.search(pattern1, line):
                msg_stat1 = True

            if re.search(pattern2, line):
                msg_stat2 = True
                break

        else:
            print("\tFAILURE")

            if msg_stat1:
                print("Did not detect Message ingested into RabbitMQ")

            print("Did not detect Valid email subject")

        if msg_stat1 and msg_stat2:
            print("\tPASS")
            os.remove(cfg.log_file)

        else:
            print("\tFAILURE")
            print("Trying to detect:  %s and %s" % (pattern1, pattern2))
            print("Log file:  %s" % (hold))

    else:
        print("\tFAILURE")
        print("Failed to load configuration")


def main():

    """Function:  main

    Description:  Control the testing of units (functions).

    Variables:
        None

    Arguments:
        None

    """

    cfg_name = "rabbitmq"
    cfg_dir = "test/unit/mail_2_rmq/config"

    args_array = arg_parser.Arg_Parse2(sys.argv, [])

    # Test valid message.
    if "-G" in args_array:
        pattern = "INFO Valid email subject:"
        print("\nmail_2_rmq.process_message unit testing...")
        test_process_message(cfg_name, cfg_dir, pattern)

    # Test invalid message.
    elif "-B" in args_array:
        pattern = "WARNING Invalid email subject:"
        print("\nmail_2_rmq.process_message unit testing (invalid message)...")
        test_process_message(cfg_name, cfg_dir, pattern)

    # Assume test for valid message.
    else:
        pattern = "INFO Valid email subject:"
        print("\nmail_2_rmq.process_message unit testing...")
        test_process_message(cfg_name, cfg_dir, pattern)


if __name__ == "__main__":
    sys.exit(main())
