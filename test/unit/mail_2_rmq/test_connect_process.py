#!/usr/bin/python
# Classification (U)

"""Program:  test_connect_process.py

    Description:  Unit testing of connect_process in mail_2_rmq.py.

    Usage:
        cat test/unit/mail_2_rmq/test_mail.txt |
        test/unit/mail_2_rmq/test_connect_process.py

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
import lib.gen_class as gen_class
import rabbit_lib.rabbitmq_class as rabbitmq_class
import version

# Version
__version__ = version.__version__


def test_connect_process(cfg_name, cfg_dir):

    """Function:  test_connect_process

    Description:  Test mail_2_rmq.connect_process function.

    Arguments:
        (input) cfg_name -> Configuration file name.
        (input) cfg_dir -> Directory path to the configuration file.

    """

    pattern = "INFO Message ingested into RabbitMQ"
    hold = []

    cfg, status_flag = mail_2_rmq.load_cfg(cfg_name, cfg_dir)

    if status_flag:

        if os.path.isfile(cfg.log_file):
            os.remove(cfg.log_file)

        LOG = gen_class.Logger(cfg.log_file, cfg.log_file, "INFO",
                               "%(asctime)s %(levelname)s %(message)s",
                               "%Y-%m-%dT%H:%M:%SZ")

        LOG.log_info("Parsing email...")
        msg = mail_2_rmq.parse_email()

        RQ = rabbitmq_class.RabbitMQPub(cfg.user, cfg.passwd, cfg.host,
                                        cfg.port, cfg.exchange_name,
                                        cfg.exchange_type, msg["subject"],
                                        msg["subject"], cfg.x_durable,
                                        cfg.q_durable, cfg.auto_delete)

        mail_2_rmq.connect_process(RQ, LOG, cfg, msg)

        LOG.log_close()

        f_hdlr = open(cfg.log_file, "r")

        for line in f_hdlr:
            hold.append(line)

            if re.search(pattern, line):
                print("\tPASS")
                os.remove(cfg.log_file)
                break

        else:
            print("\tFAILURE")
            print("Did not detect injest into RabbitMQ")
            print("Trying to detect:  %s" % (pattern))
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

    print("\nmail_2_rmq.connect_process unit testing...")
    test_connect_process(cfg_name, cfg_dir)


if __name__ == "__main__":
    sys.exit(main())
