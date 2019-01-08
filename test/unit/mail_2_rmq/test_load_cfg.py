#!/usr/bin/python
# Classification (U)

"""Program:  test_load_cfg.py

    Description:  Unit testing of load_cfg in mail_2_rmq.py.

    Usage:
        test/unit/mail_2_rmq/test_load_cfg.py

    Arguments:
        None

"""

# Libraries and Global Variables

# Standard
import sys
import os

# Third-party

# Local
sys.path.append(os.getcwd())
import mail_2_rmq
import version

# Version
__version__ = version.__version__


def test_load_cfg(cfg_name, cfg_dir):

    """Function:  test_load_cfg

    Description:  Test mail_2_rmq.load_cfg function.

    Arguments:
        (input) cfg_name -> Configuration file name.
        (input) cfg_dir -> Directory path to the configuration file.

    """

    err_queue = "isse_error_test"
    port = 5672
    exchange_name = "isse-guard-test"

    cfg, status_flag = mail_2_rmq.load_cfg(cfg_name, cfg_dir)

    if status_flag:

        if cfg.err_queue == err_queue and cfg.port == port \
           and cfg.exchange_name == exchange_name:

            print("\tPASS")

        else:
            print("\tFAILURE")
            print("Looking for \n\tHOST: %s\n\tPORT: %s\n\tEXCHANGE: %s"
                  % (host, port, exchange_name))
            print("Found \n\tHOST: %s\n\tPORT: %s\n\tEXCHANGE: %s"
                  % (cfg.host, cfg.port, cfg.exchange_name))

    else:
        print("\tFAILURE")
        print("Status flag came back as False")


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

    print("\nmail_2_rmq.load_cfg unit testing...")
    test_load_cfg(cfg_name, cfg_dir)


if __name__ == "__main__":
    sys.exit(main())
