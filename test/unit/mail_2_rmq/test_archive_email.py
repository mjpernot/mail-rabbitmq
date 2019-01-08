#!/usr/bin/python
# Classification (U)

"""Program:  test_archive_email.py

    Description:  Unit testing of archive_email in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/test_archive_email.py

    Arguments:
        None

"""

# Libraries and Global Variables

# Standard
import sys
import os
import glob

# Third-party

# Local
sys.path.append(os.getcwd())
import mail_2_rmq
import lib.gen_class as gen_class
import rabbit_lib.rabbitmq_class as rabbitmq_class
import version

# Version
__version__ = version.__version__


def test_archive_email(cfg_name, cfg_dir):

    """Function:  test_archive_email

    Description:  Test mail_2_rmq.archive_email function.

    Arguments:
        (input) cfg_name -> Configuration file name.
        (input) cfg_dir -> Directory path to the configuration file.

    """

    msg = "This is a test message"

    cfg, status_flag = mail_2_rmq.load_cfg(cfg_name, cfg_dir)

    if status_flag:
        LOG = gen_class.Logger(cfg.log_file, cfg.log_file, "INFO",
                               "%(asctime)s %(levelname)s %(message)s",
                               "%Y-%m-%dT%H:%M:%SZ")

        RQ = rabbitmq_class.RabbitMQPub(cfg.user, cfg.passwd, cfg.host,
                                        cfg.port, cfg.exchange_name,
                                        cfg.exchange_type, cfg.err_queue,
                                        cfg.err_queue, cfg.x_durable,
                                        cfg.q_durable, cfg.auto_delete)

        mail_2_rmq.archive_email(RQ, LOG, cfg, msg)

        LOG.log_close()

        filesearch = cfg.email_dir + "/" + cfg.exchange_name + "-" \
            + cfg.err_queue + "*"

        filelist = glob.glob(filesearch)

        if filelist:

            if len(filelist) == 1:
                print("\tPASS")

                for x in filelist:
                    os.remove(x)

                os.remove(cfg.log_file)

            else:
                print("\tERROR")
                print("More than one file detected:  %s" % (filelist))

        else:
            print("\tFAILURE")
            print("Empty directory detected in: %s" % (cfg.email_dir))

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

    print("\nmail_2_rmq.archive_email unit testing...")
    test_archive_email(cfg_name, cfg_dir)


if __name__ == "__main__":
    sys.exit(main())
